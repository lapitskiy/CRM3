import requests
import datetime

from owm.utils.db_utils import db_check_awaiting_postingnumber, db_get_awaiting
from owm.utils.ms_utils import ms_get_product

import locale
import pymorphy2

import logging
from typing import Dict, Any

logger_info = logging.getLogger('crm3_info')
logger_error = logging.getLogger('crm3_error')

def ozon_update_inventory(headers,stock):
    warehouseID = ozon_get_warehouse(headers)
    url = 'https://api-seller.ozon.ru/v2/products/stocks'
    ozon_stocks = []
    #print(f'update_inventory_ozon stock {stock}')
    invalid_offer_ids = []


    for key, value in stock.items():
        if value and 'stock' in value:
            if value['stock'] < 0:
                invalid_offer_ids.append(key)
                value['stock'] = 0  # Замена значения на 0
            dict_ = {
                'offer_id': key,
                'stock': value['stock'],
                'warehouse_id': warehouseID['ozon_warehouses']
                }
            ozon_stocks.append(dict_)
        else:
            print(f"Пропущен ключ {key} из-за отсутствия данных 'stock' или пустого словаря.")
    for i in range(0,len(ozon_stocks),100):
        data = {
            'stocks': ozon_stocks[i:i+99],
        }
    #print('#####')
    #print('#####')
    #print('#####')
    #print(f'ozon_data #### {data}')
    #print(f'data stock {data}')
    response = requests.post(url, headers=headers['ozon_headers'], json=data)
    context = {
        'code': response.status_code,
        'json': response.json(),
        'invalid': invalid_offer_ids
    }
    #print(f'OZON response {response.json()}')
    return context

def ozon_get_warehouse(headers):
    result = {}
    url = 'https://api-seller.ozon.ru/v1/warehouse/list'
    response = requests.post(url, headers=headers['ozon_headers']).json()
    #print(f'OZON get_warehouse {response}')
    result['ozon_warehouses'] = response['result'][0]['warehouse_id']
    return result

def ozon_get_awaiting_fbs(headers: dict):
    '''
    получаем последние отгрузки FBS (отправления)
    '''
    result = {}

    current_date = datetime.datetime.now()

    # Вычисляем дату неделю назад
    one_week_ago = current_date - datetime.timedelta(weeks=4)

    # Форматируем даты в строковый формат (YYYY-MM-DD)
    current_date_str = current_date.strftime('%Y-%m-%dT%H:%M:%SZ')
    one_week_ago_str = one_week_ago.strftime('%Y-%m-%dT%H:%M:%SZ')

    ozon_headers = headers.get('ozon_headers')
    # оприходование
    url_awaiting = 'https://api-seller.ozon.ru/v3/posting/fbs/unfulfilled/list'
    params_awaiting = {
        "filter": {
            "delivering_date_from": one_week_ago_str,
            "delivering_date_to": current_date_str,
            "is_quantum": False,
            "status": 'awaiting_approve',
            "warehouse_id": []
        },
        "dir": "DESC",
        "limit": 1000,
        "offset": 0,
        "with": {
            "analytics_data": False,
            "barcodes": False,
            "financial_data": False,
            "translit": False
        }
        }
    # awaiting_deliver - ожидает отгрузки
    url_packag = 'https://api-seller.ozon.ru/v3/posting/fbs/list'
    params_packag = {
        "filter": {
            "is_quantum": False,
            "last_changed_status_date": {
                "from": one_week_ago_str,
                "to": current_date_str
            },
            # "order_id": 0,
            "since": one_week_ago_str,
            "status": 'awaiting_packaging',  # awaiting_deliver
            "to": current_date_str,
        },
        "dir": "DESC",
        "limit": 1000,
        "offset": 0,
        "with": {
            "analytics_data": False,
            "barcodes": False,
            "financial_data": False,
            "translit": False
        }
    }

    params_deliver = {
        "filter": {
            "is_quantum": False,
            "last_changed_status_date": {
                "from": one_week_ago_str,
                "to": current_date_str
            },
            #"order_id": 0,
            "since": one_week_ago_str,
            "status": 'awaiting_deliver', #awaiting_deliver
            "to": current_date_str,
        },
        "dir": "DESC",
        "limit": 1000,
        "offset": 0,
        "with": {
            "analytics_data": False,
            "barcodes": False,
            "financial_data": False,
            "translit": False
        }
        }

    try:
        response = requests.post(url_packag, headers=ozon_headers, json=params_packag)
        if response.status_code == 200:
            packag = response.json()
            #print(f"response_json (awaiting): {awaiting}")
        else:
            result['error'] = response.text
            print(f"ozon_get_awaiting_fbs response.text (awaiting): {response.text}")
    except Exception as e:
        result['error'] = f"Error in awaiting request: {e}"

    try:
        response = requests.post(url_packag, headers=ozon_headers, json=params_deliver)
        if response.status_code == 200:
            deliver = response.json()
            #print(f"response_json (packag): {deliver}")
        else:
            result['error'] = response.text
    except Exception as e:
        result['error'] = f"Error in packag request: {e}"


    current_product = []
    #print(f'*' * 40)
    #print(f"packag {packag}")
    #print(f"awaiting {awaiting}")
    #print(f'*' * 40)

    awaiting_packag = deliver['result']['postings']
    awaiting_packag.extend(packag['result']['postings'])

    for pack in awaiting_packag:
        product_list = []
        #print(f'pack {pack}')
        posting_number = pack['posting_number']
        status = pack['status']
        #print(f"Posting Number: {posting_number}")
        for product in pack['products']:
            price = product['price']
            offer_id = product['offer_id']
            quantity =  product['quantity']
            # "sku": 1728663479,
            product_list.append({
                "offer_id": offer_id,
                "price": price,
                "quantity": quantity
                })
        current_product.append(
            {'posting_number': posting_number,
             'status': status,
             'product_list': product_list
             })


    posting_numbers = [item['posting_number'] for item in current_product]
    check_result_dict = db_check_awaiting_postingnumber(posting_numbers)
    check_result_dict['current_product'] = current_product
    return check_result_dict

def ozon_get_status_fbs(headers: Dict[str, Any]):
    '''
    получаем последние статусы заказов FBS
    '''
    result = {}
    current_date = datetime.datetime.now()
    one_week_ago = current_date - datetime.timedelta(weeks=4)
    current_date_str = current_date.strftime('%Y-%m-%dT%H:%M:%SZ')
    one_week_ago_str = one_week_ago.strftime('%Y-%m-%dT%H:%M:%SZ')

    orders_db = db_get_awaiting(market='ozon')
    # Получаем список заказов для 'ozon'
    orders_list = orders_db.get('ozon', [])
    existing_orders = {order['posting_number'] for order in orders_list}




    ozon_headers = headers.get('ozon_headers')
    url_orders = 'https://api-seller.ozon.ru/v3/posting/fbs/list'

    params = {
        "filter": {
            "is_quantum": False,
            "last_changed_status_date": {
                "from": one_week_ago_str,
                "to": current_date_str
            },
            # "order_id": 0,
            "since": one_week_ago_str,
            #"status": 'awaiting_packaging',  # awaiting_deliver
            "to": current_date_str,
        },
        "dir": "DESC",
        "limit": 1000,
        "offset": 0,
        "with": {
            "analytics_data": False,
            "barcodes": False,
            "financial_data": False,
            "translit": False
        }
    }

    matching_orders = {}
    try:
        response = requests.post(url_orders, headers=ozon_headers, json=params)
        if response.status_code == 200:
            json_orders = response.json()
            #print(f"response_json (awaiting): {awaiting}")
            json_orders = json_orders['result']['postings']
            matching_orders['delivering'] = []
            matching_orders['received'] = []
            matching_orders['cancelled'] = []
            delivering = []
            received = []
            cancelled = []
            for order in json_orders:
                posting_number = order['posting_number']
                status = order['status']
                substatus = order['substatus']
                if posting_number in existing_orders and existing_orders[posting_number] != status:
                    if 'delivering' in status and substatus != 'posting_received':
                        delivering.append({
                            'posting_number': posting_number,
                            'status': status,
                            'substatus': substatus
                        })
                    if 'posting_received' in substatus:
                        received.append({
                            'posting_number': posting_number,
                            'status': status,
                            'substatus': substatus
                        })
                    if 'cancelled' in status:
                        cancelled.append({
                            'posting_number': posting_number,
                            'status': status,
                            'substatus': substatus
                        })

            matching_orders['delivering'] = delivering
            matching_orders['received'] = received
            matching_orders['cancelled'] = cancelled
        else:
            result['error'] = response.text
            print(f"ozon_get_status_fbs response.text (awaiting): {response.text}")
    except Exception as e:
        result['error'] = f"Error in awaiting request: {e}"

    return matching_orders


def ozon_get_finance(headers: dict, period: str):
    products = ms_get_product(headers)
    opt_price_clear = {}
    print(f"products {products}")
    if products['status_code'] != 200:
        return {'error': products}

    for item in products['response']['rows']:
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
    #print(f"opt_price_clear {opt_price_clear}")

    for item in response.get('result', {}).get('rows', []):
        offer_id = item['item'].get('offer_id')
        if offer_id not in opt_price_clear:
            continue
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

def ozon_get_all_price(headers):
    opt_price = ms_get_product(headers)
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

    #print(f"ozon_headers: {headers['ozon_headers']}")
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

    #print(f"realization {realization}")

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

