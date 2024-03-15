import requests
import datetime

def get_headers(user):
    headers = {}
    if user.moysklad_api:
        headers['moysklad_headers'] = {
            "Authorization": f"Bearer {user.moysklad_api}",
        }
    if user.yandex_api:
        headers['yandex_headers'] = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {user.yandex_api}'
        }
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
        stock_tuple[stock['article']] = {'stock': stock['stock'], 'price' : stock['salePrice']/100 }
    return stock_tuple

def sort_stock_and_invent(invent_dict, stock):
    #print(f"invent_dict {invent_dict}")
    #print(f"stock {stock}")
    loss_dict = {}
    enter_dict = {}
    for key, value in stock.items():
        #print(f"key {key};   value {value};   invent dict {invent_dict[key]}")
        if key in invent_dict and float(value['stock']) > float(invent_dict[key]['stock']):
            loss_dict[key] = {}
            loss_dict[key]['stock'] = float(value['stock'])-float(invent_dict[key]['stock'])
        if key in invent_dict and float(value['stock']) < float(invent_dict[key]['stock']):
            enter_dict[key] = {}
            enter_dict[key]['stock'] = float(invent_dict[key]['stock'])-float(value['stock'])
    return enter_dict, loss_dict

# инветаризируем (оприходуем и списываем) товары на мойсклад и обновляем остатки на маркетплейсах
def inventory_update(user, invent_dict):
    headers = get_headers(user)
    stock = get_all_moysklad_stock(headers['moysklad_headers'])
    enter_dict, loss_dict = sort_stock_and_invent(invent_dict, stock)
    response = update_inventory_moysklad(headers['moysklad_headers'], enter_dict, loss_dict)
    # если мойсклад обновил, то делаем на озоне синхронизацию
    if response.status_code == 200:
        stock = get_all_moysklad_stock(headers['moysklad_headers']) # вызываем снова, так как остатки изменились
        update_inventory_ozon(headers['ozon_headers'], stock)
        update_inventory_yandex(headers['yandex_headers'], stock)
        update_inventory_wb(headers['wildberries_headers'], stock)
    user.replenishment = False
    user.save()

# инвентаризация товара мой склад
def update_inventory_moysklad(headers, enter_dict, loss_dict):
    url = 'https://api.moysklad.ru/api/remap/1.2/entity/enter'
    data = {
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
    url = 'https://api-seller.ozon.ru/v1/product/import/stocks'
    ozon_stocks = []
    for key, value in stock.items():
        ozon_stocks.append({
            'offer_id': key,
            'stock': value['stock']
            })
    for i in range(0,len(ozon_stocks),100):
        data = {
            'stocks': ozon_stocks[i:i+99],
        }
    response = requests.post(url, headers=headers, json=data).json()
    #print(f'ozon response {response}')

# инвентаризация товара яндекс
def update_inventory_yandex(headers, stock):
    url = 'https://api.partner.market.yandex.ru/campaigns'
    response = requests.get(url, headers=headers).json()
    #print(f'yandex response {response}')
    #print(f'yandex headers {headers}')
    company_id = response['campaigns'][0]['id']
    businessId = response['campaigns'][0]['business']['id']
    url = f'https://api.partner.market.yandex.ru/businesses/{businessId}/warehouses'
    response = requests.get(url, headers=headers).json()
    warehouseId = response['result']['warehouses'][0]['id']
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
    response = requests.put(url=url, json=data, headers=headers).json()
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
                'withPhoto': 1
            }
        }
    }

    while True:
        print(f"data {data}")
        while True:
            try:
                response = requests.post(url, json=data, headers=headers).json()
                print(f"response try")
                break
            except requests.exceptions.JSONDecodeError:
                print(f"exc")
        print(f"wb article response {response['cursor']}")
        print(f"total {response['cursor']['total']}")
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
    print(f'stock {len(stock)}')
    url = 'https://suppliers-api.wildberries.ru/api/v3/warehouses'
    response = requests.get(url, headers=headers).json()
    warehouseId = response[0]['id']
    url = f'https://suppliers-api.wildberries.ru/api/v3/stocks/{warehouseId}'
    sku = []
    print(f'stock {stock}')
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
    print(f'wb response status {response.status_code}')
    #print(f'wb response {response.json()}')

def get_inventory_row_data(headers, offer_dict):
    #url = f'https://api.moysklad.ru/api/remap/1.2/entity/assortment?filter=article={article}'
    url = f'https://api.moysklad.ru/api/remap/1.2/entity/assortment'
    response = requests.get(url, headers=headers).json()
    #print(f'get_prod_meta {response[']}')
    data = []
    for row in response['rows']:
        if row['article'] in offer_dict:
            data.append({
                "quantity": float(offer_dict[row['article']]['stock']),
                "assortment": {
                    "meta": row['meta']
                },
            },)
        #print(f"{row['article']}")
    #print(f'offer_dict {offer_dict}')
    #meta = response['rows'][0]['meta']
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

# создание dict из POST запроса для инвенаризации (inventory)
def inventory_POST_to_offer_dict(post):
    offer_dict = {}
    for key, value in post.items():
        if value == 'offer_id':
            stock = post[key+'_stock'] # convert float format from ',' to '.'
            offer_dict[key] = {'stock' : stock.replace(',', '.')}
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

    url = "https://api-seller.ozon.ru/v1/finance/realization"
    now = datetime.datetime.now()
    lastmonth_date = now - datetime.timedelta(days=now.day)
    data = {
        "date": lastmonth_date.strftime('%Y-%m')
        }
    response = requests.post(url, headers=headers['ozon_headers'], json=data).json()
    #print(f"date resp {response}")
    realization = {}
    for item in response['result']['rows']:
        if item['offer_id'] in realization:
            realization[item['offer_id']]['sale_qty'] = realization[item['offer_id']]['sale_qty'] + item['sale_qty']
        else:
            realization[item['offer_id']] = {'sale_qty': item['sale_qty']}
    #print(f"realization {realization}")
    #print(f"date resp {response}")

    url = "https://api-seller.ozon.ru/v4/product/info/prices"
    data = {
        "filter": {
            "visibility": "IN_SALE",
        },
            "last_id": "",
            "limit": 1000
        }
    response = requests.post(url, headers=headers['ozon_headers'], json=data).json()
    print(f"response {response['result']['items'][0]}")
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
        #print(f"{item['offer_id']} {delivery_price}")
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

# обновление цены товара озон
def update_price_ozon(obj, offer_dict):
    url = 'https://api-seller.ozon.ru/v1/product/import/prices'
    headers = get_headers(obj)
    ozon_price = []
    for key, value in offer_dict.items():
        ozon_price.append({
            'auto_action_enabled': 'ENABLED',
            'min_price': str(value['min_price']),
            'offer_id': key,
            'old_price': str(int(float(value['price']) * 2)),
            'price': str(value['price']),
            'price_strategy_enabled': 'ENABLED'
            })

    for i in range(0, len(ozon_price), 1000):
        data = {
            'prices': ozon_price[i:i+999],
        }
        response = requests.post(url, headers=headers['ozon_headers'], json=data)
    print(f'ozon price response {response.status_code}')
    print(f'ozon price json {response.json()}')
