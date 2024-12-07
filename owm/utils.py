import fnmatch

import requests
import datetime
import numpy as np
import uuid
import xlsxwriter
import locale
import pymorphy2
import os
from django.conf import settings

import pandas as pd

from collections import OrderedDict

def get_headers(user):
    headers = {}
    if user.moysklad_api:
        headers['moysklad_headers'] = {
            "Authorization": f"Bearer {user.moysklad_api}",
        }
    if user.yandex_api:
        headers['yandex_headers'] = {
            "Api-Key": user.yandex_api,
            "Content-Type": "application/json"
        }

        url = 'https://api.partner.market.yandex.ru/campaigns'
        response = requests.get(url, headers=headers['yandex_headers']).json()
        headers['yandex_id'] = {
           'company_id': response['campaigns'][0]['id'],
           'businessId': response['campaigns'][0]['business']['id']}
        url = f"https://api.partner.market.yandex.ru/businesses/{headers['yandex_id']['businessId']}/warehouses"
        response = requests.get(url, headers=headers['yandex_headers']).json()
        headers['yandex_id'].update({
            'warehouseId': response['result']['warehouses'][0]['id']
                })
    if user.ozon_api and user.client_id:
        headers['ozon_headers'] = {
            'Client-Id': user.client_id,
            'Api-Key': user.ozon_api
        }
    if user.wildberries_api:
        headers['wildberries_headers'] = {
            'Authorization': user.wildberries_api
        }
    return headers

def get_warehouse(headers):
    result = {}
    url = 'https://api-seller.ozon.ru/v1/warehouse/list'
    response = requests.post(url, headers=headers['ozon_headers']).json()
    #print(f'OZON get_warehouse {response}')
    result['ozon_warehouses'] = response['result'][0]['warehouse_id']
    return result

def get_organization_meta(headers):
    url = 'https://api.moysklad.ru/api/remap/1.2/entity/organization'
    response = requests.get(url, headers=headers).json()
    return response['rows'][0]['meta']

def get_store_meta(headers):
    url = 'https://api.moysklad.ru/api/remap/1.2/entity/store'
    response = requests.get(url, headers=headers).json()
    return response['rows'][0]['meta']

def get_all_moysklad_stock(headers):
    stock_tuple = {}
    url = "https://api.moysklad.ru/api/remap/1.2/report/stock/all"
    params = [
        ("filter", "quantityMode=all")
    ]
    response = requests.get(url, headers=headers, params=params).json()
    #print(f'response {response}')
    for stock in response['rows']:
        stock_tuple[stock['article']] = {'stock': int(stock['stock']), 'price' : stock['salePrice']/100 }
    sorted_stock_tuple = OrderedDict(sorted(stock_tuple.items()))
    return sorted_stock_tuple

def sort_stock_and_invent(invent_dict, stock):
    #print(f"invent_dict {invent_dict}")
    #print(f"stock {stock}")
    loss_dict = {}
    enter_dict = {}
    print(f'invent_dict TYT {invent_dict}')
    print(f'sort_stock_and_invent stock {stock}')
    for key, value in stock.items():
        #if key in invent_dict:
            #print(f"float(value['stock'] {float(value['stock'])} > {float(invent_dict[key]['stock'])}")
        #print(f"key {key};   value {value};   invent dict {invent_dict[key]}")
        if key in invent_dict:
            if float(value['stock']) > float(invent_dict[key]['stock']):
                loss_dict[key] = {}
                loss_dict[key]['stock'] = float(value['stock'])-float(invent_dict[key]['stock'])
            if float(value['stock']) < float(invent_dict[key]['stock']):
                enter_dict[key] = {}
                enter_dict[key]['stock'] = float(invent_dict[key]['stock'])-float(value['stock'])
            if float(value['stock']) == float(invent_dict[key]['stock']):
                print('значения равны, обновления нет смысла делать')
    result  = {
        'enter_dict': enter_dict,
        'loss_dict': loss_dict
        }

    return result

# инветаризируем (оприходуем и списываем) товары на мойсклад и обновляем остатки на маркетплейсах
def inventory_update(user, invent_dict):
    context = {}
    headers = get_headers(user)
    stock = get_all_moysklad_stock(headers['moysklad_headers'])
    stock_dict = sort_stock_and_invent(invent_dict, stock)
    #print(f'enter_dict, loss_dict {enter_dict} and {loss_dict}')
    response = update_inventory_moysklad(headers['moysklad_headers'], stock_dict)
    # если мойсклад обновил, то делаем на озоне синхронизацию
    context['moysklad'] = {
        'code': response.status_code,
        'json': response.json()
    }
    if response.status_code == 200:
        stock = get_all_moysklad_stock(headers['moysklad_headers']) # вызываем снова, так как остатки изменились

        # Оставляем только пересечение ключей
        common_keys = invent_dict.keys() & stock.keys()
        stock = {key: stock[key] for key in common_keys}
        print(f'\n\nstock сравнение {stock}\n\n')
        context['ozon'] = update_inventory_ozon(headers, stock)
        #print(f'OZON UPDATE?')
        context['yandex'] = update_inventory_yandex(headers, stock)
        context['wb'] = update_inventory_wb(headers['wildberries_headers'], stock)
    user.replenishment = False # возвращаем возможность скрипту проверять остатки на мп и мс
    user.save()
    return context

# инвентаризация товара мой склад
# MS MS MSM SM MSMSMSMSMSMS
def update_inventory_moysklad(headers, stock_dict):
    enter_dict = stock_dict['enter_dict']
    loss_dict = stock_dict['loss_dict']
    uuid_suffix = str(uuid.uuid4())[:8]
    url = 'https://api.moysklad.ru/api/remap/1.2/entity/enter'
    data = {
        'name': f'owm-{uuid_suffix}',
        'store': {"meta": get_store_meta(headers)},
        'organization': {'meta': get_organization_meta(headers)},
        'positions': get_inventory_row_data(headers, enter_dict)
    }
    responce = requests.post(url=url, json=data, headers=headers)
    #print(f"responce moysklad {responce.json()}")

    url = 'https://api.moysklad.ru/api/remap/1.2/entity/loss'
    data = {
        'store': {"meta": get_store_meta(headers)},
        'organization': {'meta': get_organization_meta(headers)},
        'positions': get_inventory_row_data(headers, loss_dict)
    }
    responce = requests.post(url=url, json=data, headers=headers)
    #print(f"responce status {type(responce.status_code)}")
    return responce

def get_inventory_row_data(headers, offer_dict):
    # url = f'https://api.moysklad.ru/api/remap/1.2/entity/assortment?filter=article={article}'
    url = f'https://api.moysklad.ru/api/remap/1.2/entity/assortment'
    response = requests.get(url, headers=headers).json()
    #print(f'get_prod_meta {response[']}')
    #print(f'get_inventory_row_data offer_dict {offer_dict}')
    data = []
    for row in response['rows']:
        #print(f'TYT')
        if row['article'] in offer_dict:
            #print(f'TYT1')
            data.append({
                "quantity": float(offer_dict[row['article']]['stock']),
                "assortment": {
                    "meta": row['meta']
                },
            }, )
        # print(f"{row['article']}")
    #print(f'get_inventory_row_data data {data}')
    # meta = response['rows'][0]['meta']
    # data = [
    #     {
    #         "quantity": count,
    #         "price": price * 100,
    #         "assortment": {
    #             "meta": meta
    #         },
    #         "overhead": 0
    #     },
    # ]
    return data

    # url = 'https://api.moysklad.ru/api/remap/1.2/entity/inventory'
    # data = {
    #     'store': {"meta": get_store_meta(headers)},
    #     'organization': {'meta': get_organization_meta(headers)},
    #     'positions': get_inventory_row_data(headers, offer_dict)
    # }
    # responce = requests.post(url=url, json=data, headers=headers)
    #print(f"responce moysklad {responce.json()}")

# инвентаризация товара озон
def update_inventory_ozon(headers,stock):
    warehouseID = get_warehouse(headers)
    url = 'https://api-seller.ozon.ru/v2/products/stocks'
    ozon_stocks = []
    print(f'update_inventory_ozon stock {stock}')
    for key, value in stock.items():
        if value and 'stock' in value:
            ozon_stocks.append({
                'offer_id': key,
                'stock': value['stock'],
                'warehouse_id': warehouseID['ozon_warehouses']
            })
        else:
            print(f"Пропущен ключ {key} из-за отсутствия данных 'stock' или пустого словаря.")
    for i in range(0,len(ozon_stocks),100):
        data = {
            'stocks': ozon_stocks[i:i+99],
        }
    #print(f'data stock {data}')
    response = requests.post(url, headers=headers['ozon_headers'], json=data)
    context = {
        'code': response.status_code,
        'json': response.json()
    }
    #print(f'OZON response {response.json()}')
    return context

# инвентаризация товара яндекс
def update_inventory_yandex(headers, stock):
    #print(f"head {headers}")
    headers_ya = headers['yandex_headers']
    company_id = headers['yandex_id']['company_id']
    businessId = headers['yandex_id']['businessId']
    warehouseId = headers['yandex_id']['warehouseId']
    current_time = datetime.datetime.now()
    offset = datetime.timezone(datetime.timedelta(hours=3))  # Указываем смещение +03:00
    formatted_time = current_time.replace(tzinfo=offset).isoformat()
    url = f'https://api.partner.market.yandex.ru/campaigns/{company_id}/offers/stocks'
    sku = []
    for key, value in stock.items():
        sku.append({
            'sku': key,
            'warehouseId': warehouseId,
            'items': [{
                'count': int(value['stock']),
                'type': 'FIT',
                'updatedAt': formatted_time
            }]
        })
    data = {
        'skus': sku
    }
    #print(f"skus {data['skus'][0]}")
    response = requests.put(url=url, json=data, headers=headers_ya)
    context = {
        'code': response.status_code,
        'json': response.json()
    }
    return context
    #print(f'yandex response 2 {response}')

# инвентаризация товара яндекс
def update_inventory_wb(headers, stock):
    url = 'https://suppliers-api.wildberries.ru/content/v2/get/cards/list'
    #url = 'https://content-api-sandbox.wildberries.ru/content/v2/get/cards/list'
    data = {
        'settings': {
            'cursor': {
                'limit': 100,
            },
            'filter': {
                'withPhoto': -1
            }
        }
    }

    while True:
        #print(f"data {data}")
        while True:
            try:
                response = requests.post(url, json=data, headers=headers).json()
                print(f"response try")
                break
            except requests.exceptions.JSONDecodeError:
                print(f"exc")
        #print(f"wb article response {response['cursor']}")
        #print(f"total {response['cursor']['total']}")
        #print(f"response {response}")
        for item in response['cards']:
            if item['vendorCode'] in stock:
                stock[item['vendorCode']]['sku'] = item['sizes'][0]['skus'][0]
        data = {
            'settings': {
                'cursor': {
                    'updatedAt': response['cursor']['updatedAt'],
                    'nmID': response['cursor']['nmID'],
                    'limit': 100,
                },
                'filter': {
                    'withPhoto': 1
                }
            }
        }
        if response['cursor']['total'] < 100: break
    #print(f'stock {len(stock)}')
    url = 'https://suppliers-api.wildberries.ru/api/v3/warehouses'
    response = requests.get(url, headers=headers).json()
    warehouseId = response[0]['id']
    url = f'https://suppliers-api.wildberries.ru/api/v3/stocks/{warehouseId}'
    sku = []
    #print(f'stock {stock}')
    for key, value in stock.items():
        if 'sku' in value:
            sku.append({
                'sku': value['sku'],
                'amount': int(value['stock'])
                })
    data = {
        'stocks': sku
    }
    response = requests.put(url, json=data, headers=headers)
    #print(f'wb response {response}')
    #print(f'wb response status {response.status_code}')
    #print(f'wb response text {response.text}')
    if response.status_code == 204:
        json = 'Update'
    else:
        json = response.json()
    context = {
        'code': response.status_code,
        'json': json
    }
    return context
    #print(f'wb response {response.json()}')


# создание dict из POST запроса для инвенаризации (inventory)
def inventory_POST_to_offer_dict(post_data):
    offer_dict = {}

    # Обрабатываем все данные из словаря post_data
    for key, value in post_data.items():
        if key.endswith("_checked"):  # Проверяем только чекбоксы
            offer_id = key.replace("_checked", "")  # Извлекаем offer_id
            is_checked = value == "on"
            stock_value = post_data.get(f"{offer_id}_stock", None)  # Получаем значение stock

            if is_checked:
                offer_dict[offer_id] = {'stock' : f"{float(stock_value):.1f}".replace(',', '.')}
    return offer_dict

def get_moysklad_opt_price(headers):
    stock_tuple = {}
    url = "https://api.moysklad.ru/api/remap/1.2/entity/product"
    params = [
        ("limit", 1000)
    ]
    response = requests.get(url, headers=headers, params=params).json()
    return response

def get_all_price_ozon(headers):
    opt_price = get_moysklad_opt_price(headers['moysklad_headers'])
    #print(f"opt_price {opt_price['rows'][0]['buyPrice']['value']}")
    #print(f"opt_price {opt_price['rows'][0]['article']}")
    opt_price_clear = {}
    for item in opt_price['rows']:
        #opt_price_clear['article'] = item['article']
        #print(f"opt_price {item['buyPrice']['value']/100}")
        opt_price_clear[item['article']] = {
            'opt_price' : int(float(item['buyPrice']['value']) / 100),
            }

    url = "https://api-seller.ozon.ru/v2/finance/realization"
    now = datetime.datetime.now()
    lastmonth_date = now - datetime.timedelta(days=now.day)
    data = {
        "year": lastmonth_date.year,
        "month": lastmonth_date.month
    }

    print(f"ozon_headers: {headers['ozon_headers']}")
    response = requests.post(url, headers=headers['ozon_headers'], json=data).json()
    #print(f"utils.py | get_all_price_ozon | response: {response}")
    realization = {}
    for item in response.get('result', {}).get('rows', []):
        offer_id = item['item'].get('offer_id')
        quantity = item['delivery_commission']['quantity'] if item.get('delivery_commission') and 'quantity' in item['delivery_commission'] else 0

        # Инициализируем, если offer_id нет в realization или оно равно None
        if offer_id not in realization or realization[offer_id] is None:
            realization[offer_id] = {'sale_qty': quantity}
        else:
            # Добавляем к sale_qty, если offer_id уже существует
            realization[offer_id]['sale_qty'] = realization[offer_id].get('sale_qty', 0) + quantity

    print(f"realization {realization}")

    url = "https://api-seller.ozon.ru/v4/product/info/prices"
    data = {
        "filter": {
            "visibility": "IN_SALE",
        },
            "last_id": "",
            "limit": 1000
        }
    response = requests.post(url, headers=headers['ozon_headers'], json=data).json()
    #print(f"response {response['result']['items'][0]}")
    result = {}
    for item in response['result']['items']:
        #print(f'item {item}')
        if item['offer_id'] not in opt_price_clear:
            continue
        if item['offer_id'] not in realization:
            realization[item['offer_id']] = {'sale_qty': 0}
        delivery_price = float(item['price']['marketing_seller_price'])/100 * float(item['commissions']['sales_percent_fbs'])
        delivery_price = delivery_price + float(item['commissions']['fbs_direct_flow_trans_min_amount']) \
                         + float(item['commissions']['fbs_deliv_to_customer_amount']) + \
                         float(item['price']['marketing_seller_price'])/100*1 # эквайринг 1% и 10% для средней цены
        delivery_price = delivery_price + 15 # средняя цена доставки товара
        #print(f"opt_price {item['offer_id']}")
        profit_price = int(float(item['price']['marketing_seller_price'])) - \
                       int(delivery_price) - opt_price_clear[item['offer_id']]['opt_price']
        profit_percent = profit_price / opt_price_clear[item['offer_id']]['opt_price'] * 100
        min_price = float(item['price']['min_price'])
        min_price_percent30 = int(delivery_price) + (opt_price_clear[item['offer_id']]['opt_price'] * 1.3)
        min_price_percent50 = int(delivery_price) + (opt_price_clear[item['offer_id']]['opt_price'] * 1.5)
        min_price_percent80 = int(delivery_price) + (opt_price_clear[item['offer_id']]['opt_price'] * 1.8)
        min_price_percent100 = int(delivery_price) + (opt_price_clear[item['offer_id']]['opt_price'] * 2)
        #print(f"offer_id {item}")
        result[item['offer_id']] = {
            'product_id': int(float(item['product_id'])),
            'min_price': int(min_price),
            'min_price_percent30': int(min_price_percent30),
            'min_price_percent50': int(min_price_percent50),
            'min_price_percent80': int(min_price_percent80),
            'min_price_percent100': int(min_price_percent100),
            'marketing_seller_price': int(float(item['price']['marketing_seller_price'])),
            'delivery_price': int(delivery_price),
            'opt_price': opt_price_clear[item['offer_id']]['opt_price'],
            'profit_price': profit_price,
            'profit_percent': int(profit_percent),
            'sale_qty': realization[item['offer_id']]['sale_qty']
        }


    #print(f'result ozon price {result}')
    return result

def get_all_price_wb(headers):
    result = {}
    opt_price = get_moysklad_opt_price(headers['moysklad_headers'])
    #print(f"opt_price {opt_price['rows'][0]['buyPrice']['value']}")
    #print(f"opt_price {opt_price['rows'][0]['article']}")
    opt_price_clear = {}
    for item in opt_price['rows']:
        #opt_price_clear['article'] = item['article']
        #print(f"opt_price {item['buyPrice']['value']/100}")
        opt_price_clear[item['article']] = {
            'opt_price' : int(float(item['buyPrice']['value']) / 100),
            }

    # продажи за последние 30 дней
    #url = "https://statistics-api.wildberries.ru/api/v1/supplier/sales"
    url = "https://statistics-api.wildberries.ru/api/v3/supplier/reportDetailByPeriod"
    dateTo = datetime.datetime.now()
    dateFrom = dateTo - datetime.timedelta(days=+30)
    dateTo = dateTo.strftime('%Y-%m-%d')
    dateFrom = dateFrom.strftime('%Y-%m-%d')
    print(f"date RFC3339 {dateTo}") #.isoformat()
    data = {
        'dateFrom': dateFrom, #lastmonth_date.strftime('%Y-%m')
        'dateTo': dateTo,
        'limit': 100
        }
    print(f"data wb {data}")
    response = requests.get(url, headers=headers['wildberries_headers'], json=data).json()
    print(f"date resp wb json {response}")
    realization = {}
    if response:
        if response['code'] == 503:
            result['error'] = response['message']

        if response['code'] == 200:
            for item in response['result']['rows']:
                if item['offer_id'] in realization:
                    realization[item['offer_id']]['sale_qty'] = realization[item['offer_id']]['sale_qty'] + item['sale_qty']
                else:
                    realization[item['offer_id']] = {'sale_qty': item['sale_qty']}
    #print(f"realization {realization}")
    #print(f"date resp {response}")

    url = "https://discounts-prices-api.wb.ru/api/v2/list/goods/filter"
    data = {
            'limit': 10,
            'offset': 0
            }
    response = requests.get(url, headers=headers['wildberries_headers'], json=data).json()
    print(f"response wb {response}")
    result = {}
    for item in response['result']['items']:
        if item['offer_id'] not in opt_price_clear:
            continue
        if item['offer_id'] not in realization:
            realization[item['offer_id']] = {'sale_qty': 0}
        delivery_price = float(item['price']['marketing_seller_price'])/100 * float(item['commissions']['sales_percent_fbs'])
        delivery_price = delivery_price + float(item['commissions']['fbs_direct_flow_trans_min_amount']) \
                         + float(item['commissions']['fbs_deliv_to_customer_amount']) + \
                         float(item['price']['marketing_seller_price'])/100*1 # эквайринг 1% и 10% для средней цены
        delivery_price = delivery_price + 15 # средняя цена доставки товара
        if item['offer_id'] == 'renata_371':
            print(f"371 {item}")
        #print(f"opt_price {item['offer_id']}")
        profit_price = int(float(item['price']['marketing_seller_price'])) - \
                       int(delivery_price) - opt_price_clear[item['offer_id']]['opt_price']
        profit_percent = profit_price / opt_price_clear[item['offer_id']]['opt_price'] * 100
        min_price = int(delivery_price) + (opt_price_clear[item['offer_id']]['opt_price']/100*30) + opt_price_clear[item['offer_id']]['opt_price']

        #print(f"offer_id {item}")
        result[item['offer_id']] = {
            'price': int(float(item['price']['price'])),
            'min_price': int(min_price),
            'marketing_seller_price': int(float(item['price']['marketing_seller_price'])),
            'delivery_price': int(delivery_price),
            'opt_price': opt_price_clear[item['offer_id']]['opt_price'],
            'profit_price': profit_price,
            'profit_percent': int(profit_percent),
            'sale_qty': realization[item['offer_id']]['sale_qty']
        }

    #print(f'result ozon price {result}')
    return result


def get_all_price_yandex(headers):
    # калулутяор fbs fby https: // dev - market - partner - api.docs - viewer.yandex.ru / ru / reference / tariffs / calculateTariffs

    result = {}
    company_id = headers['yandex_id']['company_id']
    businessId = headers['yandex_id']['businessId']
    warehouseId = headers['yandex_id']['warehouseId']
    opt_price = get_moysklad_opt_price(headers['moysklad_headers'])
    # print(f"opt_price {opt_price['rows'][0]['buyPrice']['value']}")
    # print(f"opt_price {opt_price['rows'][0]['article']}")
    opt_price_clear = {}
    for item in opt_price['rows']:
        # opt_price_clear['article'] = item['article']
        # print(f"opt_price {item['buyPrice']['value']/100}")
        opt_price_clear[item['article']] = {
            'opt_price': int(float(item['buyPrice']['value']) / 100),
        }

    # продажи за последние 30 дней
    # url = "https://statistics-api.wildberries.ru/api/v1/supplier/sales"
    url = f"https://api.partner.market.yandex.ru/campaigns/{company_id}/offer-prices"
    data = {
        'limit': 100
    }
    response = requests.get(url, headers=headers['yandex_headers'], json=data).json()
    print(f"resp yandex json {response}")
    for item in response['result']['offers']:
        result[item['id']] = {
            'price': int(float(item['price']['price'])),
            'min_price': int(min_price),
            'marketing_seller_price': int(float(item['price']['marketing_seller_price'])),
            'delivery_price': int(delivery_price),
            'opt_price': opt_price_clear[item['offer_id']]['opt_price'],
            'profit_price': profit_price,
            'profit_percent': int(profit_percent),
            'sale_qty': realization[item['offer_id']]['sale_qty']
        }

    if response:
        if response['status'] == 503:
            result['error'] = response['message']

    return result


# обновление цены товара озон
def update_price_ozon(obj, offer_dict):
    url = 'https://api-seller.ozon.ru/v1/product/import/prices'
    headers = get_headers(obj)
    ozon_price = []
    for key, value in offer_dict.items():
        ozon_price.append({
            'auto_action_enabled': 'ENABLED',
            'min_price': str(value['min_price']),
            'price': str(int(value['min_price']) * 1.3),
            'offer_id': key,
            'old_price': str((int(value['min_price']) * 1.3) * 1.5),
            'price_strategy_enabled': 'DISABLED'
            })

    for i in range(0, len(ozon_price), 1000): # 1000
        data = {
            'prices': ozon_price[i:i+999],
            #'prices': ozon_price[i:i + 2],
        }
        response = requests.post(url, headers=headers['ozon_headers'], json=data)
        print(f'data {data}')
        break
    #print(f'ozon price response {response.status_code}')
    print(f'ozon price json {response.json()}')

def get_postavka_ozon(headers: dict):
    uuid_suffix = str(uuid.uuid4())[:6]

    path = os.path.join(settings.MEDIA_ROOT, 'owm/report/')
    url_path = os.path.join(settings.MEDIA_URL, 'owm/report/', f'stock_data_ozn_{uuid_suffix}.xlsx')
    file_path = os.path.join(settings.MEDIA_ROOT, 'owm/report/', f'stock_data_ozn_{uuid_suffix}.xlsx')
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    url = "https://api-seller.ozon.ru/v1/analytics/turnover/stocks"
    data = {
        "limit": 1000,
    }

    response = requests.post(url, headers=headers['ozon_headers'], json=data).json()

    rows = []
    for item in response.get('items', []):
        offer_id = item.get('offer_id')
        # Шаг 1: Считаем, сколько товара нужно на 90 дней
        total_stock_needed = 90 * item.get('ads')
        rows.append({
            'offer_id': item['offer_id'],
            'name': '',  # Имя оставляем пустым
            'stock_needed': int(round(max(0, total_stock_needed - item.get('current_stock')))) # Округляем до целого
            })

    # Создание XLSX файла

    prefix = 'stock_data'
    delete_files_with_prefix(path, prefix)

    workbook = xlsxwriter.Workbook(file_path)
    worksheet = workbook.add_worksheet()
    headers = ['Артикул', 'Имя', 'Количество']

    rows_sorted = sorted(rows, key=lambda x: x['offer_id'])  # Сортировка по 'offer_id'

    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header)
    for row_num, row in enumerate(rows_sorted, start=1):
        worksheet.write(row_num, 0, row['offer_id'])  # Артикул
        worksheet.write(row_num, 1, row['name'])  # Имя (пустое)
        worksheet.write(row_num, 2, row['stock_needed'])  # Количество
    workbook.close()

    result = {}
    result['row'] = rows_sorted
    result['path'] = url_path
    result['code'] = 8 if response.get('code') == 8 else 0
    return result
def get_finance_ozon(headers: dict, period: str):
    opt_price = get_moysklad_opt_price(headers['moysklad_headers'])
    opt_price_clear = {}
    for item in opt_price['rows']:
        #opt_price_clear['article'] = item['article']
        #print(f"opt_price {item['buyPrice']['value']/100}")
        opt_price_clear[item['article']] = {
            'opt_price' : int(float(item['buyPrice']['value']) / 100),
            }

    url = "https://api-seller.ozon.ru/v2/finance/realization"
    now = datetime.datetime.now()
    lastmonth_date = now - datetime.timedelta(days=now.day)
    data = {
        "year": lastmonth_date.year,
        "month": lastmonth_date.month
    }

    response = requests.post(url, headers=headers['ozon_headers'], json=data).json()
    #print(f"utils.py | get_all_price_ozon | response: {response}")
    #print(f"realization {response['result']['rows']}")
    result = {}
    summed_totals = {}
    header_data = response.get('result', {}).get('header', [])
    all_return_total = 0
    for item in response.get('result', {}).get('rows', []):
        offer_id = item['item'].get('offer_id')
        if item.get('return_commission') is not None:
            all_return_total += int(item['return_commission']['total'])

        if item.get('delivery_commission') is not None:
            # Получаем 'quantity' из каждого словаря с параметром по умолчанию равным 0, если ключ отсутствует
            opt = opt_price_clear[offer_id]['opt_price']
            if item.get('return_commission') is not None:
                delivery_quantity = item.get('delivery_commission').get('quantity', 0)
                return_quantity = item.get('return_commission').get('quantity', 0)
                if delivery_quantity > return_quantity:
                    new_entry = {
                        'total_price': int(item['delivery_commission']['total']) - int(item['return_commission']['total']),
                        'quantity': int(item['delivery_commission']['quantity']) - int(item['return_commission']['quantity']),
                    }
                else:
                    continue

            else:
                new_entry = {
                    'total_price': int(item['delivery_commission']['total']),
                    'quantity': int(item['delivery_commission']['quantity'])
                }
            new_entry.update({
                'name': item['item']['name'],
                'product_id': int(item['item']['sku']),
                'seller_price_per_instance': int(item['seller_price_per_instance']),
                'opt': int(opt)
            })
            net_profit = new_entry['total_price'] - (opt * new_entry['quantity'])
            net_profit_perc = (net_profit / (opt * new_entry['quantity'])) * 100 if opt * new_entry[
                'quantity'] != 0 else 0
            posttax_profit = net_profit - (new_entry['total_price'] * 0.06)
            posttax_profit_perc = (posttax_profit / (opt * new_entry['quantity'])) * 100 if opt * new_entry[
                'quantity'] != 0 else 0
            new_entry.update({
                'net_profit': net_profit,
                'net_profit_perc': int(net_profit_perc),
                'posttax_profit': posttax_profit,
                'posttax_profit_perc': int(posttax_profit_perc),
            })
            if offer_id in result:
                result[offer_id].append(new_entry)
            else:
                result[offer_id] = [new_entry]

    #print(f'result ozon price {result}')
    # seller_price_per_instance Цена продавца с учётом скидки.
    # 'item': {'offer_id': 'cer_black_20', 'barcode': 'OZN1249002486', 'sku': 1249002486},
    sorted_report = dict(sorted(result.items(), key=lambda item: (item[0][:3], item[0][3:])))

    # Итерация по результатам и вычисление суммы total_price
    for offer_id, entries in result.items():
        total_price_sum = sum(entry['total_price'] for entry in entries)
        net_profit_sum = sum(entry['net_profit'] for entry in entries)
        posttax_profit_sum = sum(entry['posttax_profit'] for entry in entries)
        total_quantity = sum(entry['quantity'] for entry in entries)

        # Расчет средней цены продажи
        average_sales_price = total_price_sum / total_quantity if total_quantity > 0 else 0

        average_percent_posttax = sum(entry['posttax_profit_perc'] for entry in entries) / len(
            entries) if entries else 0

        # Сохраняем результаты в словарь
        summed_totals[offer_id] = {
            "total_price_sum": int(total_price_sum),
            "net_profit_sum": int(net_profit_sum),
            "posttax_profit_sum": int(posttax_profit_sum),
            "average_sales_price": int(average_sales_price),
            "average_percent_posttax": int(average_percent_posttax),
            "total_quantity": int(total_quantity),
        }
    #print(f'summed_totals {summed_totals}')
    all_total_price_sum = sum(value["total_price_sum"] for value in summed_totals.values())
    all_totals = {
        "all_total_price_sum": all_total_price_sum,
        "all_net_profit_sum": sum(value["net_profit_sum"] for value in summed_totals.values()),
        "all_posttax_profit_sum": sum(value["posttax_profit_sum"] for value in summed_totals.values()),
        "all_quantity": sum(value["total_quantity"] for value in summed_totals.values()),
        "all_return_total": all_return_total
    }
    all_totals = {
        key: f"{value:,}" if isinstance(value, (int, float)) else value
        for key, value in all_totals.items()
    }



    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

    start_date = datetime.datetime.strptime(header_data['start_date'], '%Y-%m-%d')
    stop_date = datetime.datetime.strptime(header_data['stop_date'], '%Y-%m-%d')
    month_name = start_date.strftime('%B')
    morph = pymorphy2.MorphAnalyzer()
    month_nominative = morph.parse(month_name)[0].inflect({'nomn'}).word
    day_delta = stop_date - start_date
    header_data['month'] = month_nominative.capitalize()
    header_data['day_delta'] = day_delta.days

    # Выводим отсортированный словарь
    result = {}
    result['sorted_report'] = sorted_report
    result['all_totals'] = all_totals
    result['summed_totals'] = summed_totals
    result['header_data'] = header_data
    return result

def get_finance_wb(headers: dict, period: str):
    opt_price = get_moysklad_opt_price(headers['moysklad_headers'])
    opt_price_clear = {}
    for item in opt_price['rows']:
        #opt_price_clear['article'] = item['article']
        #print(f"opt_price {item['buyPrice']['value']/100}")
        opt_price_clear[item['article']] = {
            'opt_price' : int(float(item['buyPrice']['value']) / 100),
            }

    url = "https://statistics-api.wildberries.ru/api/v5/supplier/reportDetailByPeriod"
    now = datetime.datetime.now()
    # Вычисляем первый день предыдущего месяца
    first_day_of_last_month = datetime.datetime(now.year, now.month, 1) - datetime.timedelta(days=1)
    first_day_of_last_month = first_day_of_last_month.replace(day=1)
    # Вычисляем последний день предыдущего месяца
    last_day_of_last_month = first_day_of_last_month.replace(day=1) + datetime.timedelta(days=32)
    last_day_of_last_month = last_day_of_last_month.replace(day=1) - datetime.timedelta(days=1)

    #date = {
    #    "dateFrom": first_day_of_last_month.strftime('%Y-%m-%d'),
    #    "dateTo": last_day_of_last_month.strftime('%Y-%m-%d'),
    #    "limit": 10000
    #}


    date = {
        "dateFrom": "2024-11-01",
        "dateTo": "2024-11-28"
    }

    print(f'date {date}')

    response = requests.get(url, headers=headers['wildberries_headers'], params=date).json()

    count_dicts = len(response)
    print(f"Количество словарей: {count_dicts}")

    print(f'response {response}')



    translated_keys = {
        'date_from': 'Дата начала',
        'date_to': 'Дата окончания',
        #'rrd_id': 'ID записи отчета',
        #'gi_id': 'ID товарной позиции',
        'dlv_prc': 'Процент доставки',
        #'fix_tariff_date_from': 'Начало действия фиксированного тарифа',
        #'fix_tariff_date_to': 'Окончание действия фиксированного тарифа',
        'subject_name': 'Наименование товара',
        'nm_id': 'Код товара',
        #'brand_name': 'Бренд',
        'sa_name': 'Краткое имя SA',
        'ts_name': 'Имя TS',
        'barcode': 'Штрихкод',
        'doc_type_name': 'Тип документа',
        'quantity': 'Количество',
        'retail_price': 'Розничная цена',
        'retail_amount': 'Розничная сумма',
        'sale_percent': 'Процент продаж',
        'commission_percent': 'Процент комиссии',
        'supplier_oper_name': 'Операция поставщика',
        #'order_dt': 'Дата заказа',
        #'sale_dt': 'Дата продажи',
        #'rr_dt': 'Дата отчета',
        'shk_id': 'ID SHK',
        'retail_price_withdisc_rub': 'Цена с учетом скидки, RUB',
        'delivery_amount': 'Сумма доставки',
        'return_amount': 'Сумма возврата',
        'delivery_rub': 'Стоимость доставки, RUB',
        #'gi_box_type_name': 'Тип упаковки',
        'product_discount_for_report': 'Скидка на товар для отчета',
        'rid': 'RID',
        'ppvz_spp_prc': 'PPVZ SPP PRC',
        'ppvz_kvw_prc_base': 'Основа PPVZ KVW PRC',
        'ppvz_kvw_prc': 'PPVZ KVW PRC',
        #'sup_rating_prc_up': 'Повышение рейтинга поставщика',
        'is_kgvp_v2': 'Is KGVP V2',
        'ppvz_sales_commission': 'Комиссия WB',
        'ppvz_for_pay': 'К выплате',
        'ppvz_reward': 'Комиссия ПВЗ',
        'acquiring_fee': 'Комиссия за эквайринг',
        'acquiring_percent': 'Процент эквайринга',
        'payment_processing': 'Обработка платежей',
        'acquiring_bank': 'Банк эквайринга',
        'ppvz_vw': 'Вознаграждение WB',
        'ppvz_vw_nds': 'PPVZ VW НДС',
        'declaration_number': 'Номер декларации',
        'bonus_type_name': 'Тип бонуса',
        'sticker_id': 'ID стикера',
        'site_country': 'Страна сайта',
        'srv_dbs': 'SRV DBS',
        'penalty': 'Штраф',
        'additional_payment': 'Дополнительная оплата',
        'rebill_logistic_cost': 'Стоимость перевозки при пересчете',
        'storage_fee': 'Плата за хранение',
        'deduction': 'Вычет',
        'acceptance': 'Принятие',
        'assembly_id': 'ID сборки',
        'srid': 'SRID',
    }

    filtered_response = [{key: item.get(key, None) for key in translated_keys.keys()} for item in response]

    df = pd.DataFrame(filtered_response)

    result = {}
    result['path'] = {}

    uuid_suffix = str(uuid.uuid4())[:6]
    prefix = 'stock_wb'
    path = os.path.join(settings.MEDIA_ROOT, 'owm/report/')
    url_path = os.path.join(settings.MEDIA_URL, 'owm/report/', f'stock_wb_all_{uuid_suffix}.xlsx')
    root_path = os.path.join(settings.MEDIA_ROOT, 'owm/report/', f'stock_wb_all_{uuid_suffix}.xlsx')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    delete_files_with_prefix(path, prefix)
    #df.rename(columns=translated_keys, inplace=True)
    df.to_excel(root_path, index=False)

    result['path']['all'] = os.path.join(settings.MEDIA_URL, 'owm/report/', f'{url_path}')


    category_translation = {
        'Логистика': 'logistic',
        'Продажа': 'sale',
        'Возмещение': 'reimbursement',
        'Хранение': 'storage',
        'приемка': 'acceptance',
        'Возврат': 'return'
    }

    category_dfs = {
        category: df[df['supplier_oper_name'].str.contains(category, na=False)]
        for category in category_translation.keys()
    }

    summed_totals = {}
    offer_id_result = {}
    for index, row in category_dfs['Продажа'].iterrows():
        offer_id = row['sa_name']
        opt = opt_price_clear[offer_id]['opt_price']
        new_entry = {
            'name': row['subject_name'],
            'for_pay': int(row['ppvz_for_pay'],), # к выплате
            'quantity': int(row['quantity'],),  # Сумма продаж (возвратов)
            'opt': int(opt)
            }
        net_profit = new_entry['for_pay'] - (opt * new_entry['quantity']) #чистая без опта
        net_profit_perc = (net_profit / (opt * new_entry['quantity'])) * 100 if opt * new_entry['quantity'] != 0 else 0
        posttax_profit = net_profit - (new_entry['for_pay'] * 0.06)
        posttax_profit_perc = (posttax_profit / (opt * new_entry['quantity'])) * 100 if opt * new_entry['quantity'] != 0 else 0
        new_entry.update({
            'net_profit': net_profit,
            'net_profit_perc': int(net_profit_perc),
            'posttax_profit': posttax_profit,
            'posttax_profit_perc': int(posttax_profit_perc),
        })
        if offer_id in offer_id_result:
            offer_id_result[offer_id].append(new_entry)
        else:
            offer_id_result[offer_id] = [new_entry]

    # print(f'result ozon price {result}')
    # seller_price_per_instance Цена продавца с учётом скидки.
    # 'item': {'offer_id': 'cer_black_20', 'barcode': 'OZN1249002486', 'sku': 1249002486},
    sorted_report = dict(sorted(offer_id_result.items(), key=lambda item: (item[0][:3], item[0][3:])))

    # Итерация по результатам и вычисление суммы total_price
    for offer_id, entries in offer_id_result.items():
        for_pay_sum = sum(entry['for_pay'] for entry in entries)
        net_profit_sum = sum(entry['net_profit'] for entry in entries)
        posttax_profit_sum = sum(entry['posttax_profit'] for entry in entries)
        total_quantity = sum(entry['quantity'] for entry in entries)

        # Расчет средней цены продажи
        average_sales_price = for_pay_sum / total_quantity if total_quantity > 0 else 0

        average_percent_posttax = sum(entry['posttax_profit_perc'] for entry in entries) / len(entries) if entries else 0

        # Сохраняем результаты в словарь
        summed_totals[offer_id] = {
            "for_pay_sum": int(for_pay_sum),
            "net_profit_sum": int(net_profit_sum),
            "posttax_profit_sum": int(posttax_profit_sum),
            "average_sales_price": int(average_sales_price),
            "average_percent_posttax": int(average_percent_posttax),
            "total_quantity": int(total_quantity),
        }

    #print(f'summed_totals {summed_totals}')
    all_for_pay_sum = sum(value["for_pay_sum"] for value in summed_totals.values())
    all_return_total = 0
    all_return_total = int(category_dfs['Возврат']["retail_amount"].sum())
    all_totals = {
        "all_for_pay_sum": all_for_pay_sum,
        "all_net_profit_sum": sum(value["net_profit_sum"] for value in summed_totals.values()),
        "all_posttax_profit_sum": sum(value["posttax_profit_sum"] for value in summed_totals.values()),
        "all_quantity": sum(value["total_quantity"] for value in summed_totals.values()),
        "all_return_total": all_return_total
    }
    all_totals = {
        key: f"{value:,}" if isinstance(value, (int, float)) else value
        for key, value in all_totals.items()
    }

    for category, english_name in category_translation.items():
        # Создаём путь для каждого файла
        category_path = os.path.join(settings.MEDIA_ROOT,'owm/report/',f'stock_wb_{english_name}_{uuid_suffix}.xlsx')
        # Сохраняем DataFrame в Excel
        result['path'][f'{english_name}'] = os.path.join(settings.MEDIA_URL, 'owm/report/', f'stock_wb_{english_name}_{uuid_suffix}.xlsx')
        if category in category_dfs:
            category_dfs[category].to_excel(category_path, index=False)
            print(f"Файл для категории '{category}' сохранён как {result['path'][f'{english_name}']}")
        else:
            print(f"Категория '{category}' отсутствует в данных.")


    result['translated_keys'] = translated_keys
    result['date'] = date
    if isinstance(response, list):
        for item in response:
            if isinstance(item, dict) and item.get('code') == 8:
                result['code'] = 8
                break
        else:
            result['code'] = 0
    # Выводим отсортированный словарь
    result['sorted_report'] = sorted_report
    result['all_totals'] = all_totals
    result['summed_totals'] = summed_totals
    return result


def delete_files_with_prefix(directory_path, prefix):
    """
    Удаляет все файлы в указанной папке, начинающиеся с заданного префикса.
    """
    if os.path.exists(directory_path):
        for filename in os.listdir(directory_path):
            if fnmatch.fnmatch(filename, f"{prefix}*"):  # Проверяем, начинается ли имя с префикса
                file_path = os.path.join(directory_path, filename)
                try:
                    os.unlink(file_path)  # Удаляем файл
                    print(f"Удалён файл: {file_path}")
                except Exception as e:
                    print(f"Ошибка при удалении {file_path}: {e}")
    else:
        print(f"Директория {directory_path} не существует.")

def sync_inventory():
    pass

