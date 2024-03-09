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
    print(f"responce moysklad {responce.json()}")

    url = 'https://api.moysklad.ru/api/remap/1.2/entity/loss'
    data = {
        'store': {"meta": get_store_meta(headers)},
        'organization': {'meta': get_organization_meta(headers)},
        'positions': get_inventory_row_data(headers, loss_dict)
    }
    responce = requests.post(url=url, json=data, headers=headers)
    print(f"responce status {type(responce.status_code)}")
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
    print(f'yandex response {response}')
    print(f'yandex headers {headers}')
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
    print(f"skus {data['skus'][0]}")
    response = requests.put(url=url, json=data, headers=headers).json()
    print(f'yandex response 2 {response}')

# инвентаризация товара яндекс
def update_inventory_wb(headers, stock):
    url = 'https://suppliers-api.wildberries.ru/content/v2/get/cards/list'
    data = {
        'settings': {
            'cursor': {
                'limit': 20
            },
        }
    }
    response = requests.post(url, json=data, headers=headers).json()
    print(f'wb article response {response}')
    for item in response['cards']:
        if item['vendorCode'] in stock:
            stock[item['vendorCode']]['sku'] = item['sizes'][0]['skus']

    print(f'stock {stock}')
    url = 'https://suppliers-api.wildberries.ru/api/v3/warehouses'
    response = requests.get(url, headers=headers).json()
    warehouseId = response[0]['id']
    url = f'https://suppliers-api.wildberries.ru/api/v3/stocks/{warehouseId}'
    sku = []
    for key, value in stock.items():
        sku.append({
            'sku': key,
            'amount': int(value['stock'])
            })
    data = {
        'stocks': sku
    }
    response = requests.put(url, json=data, headers=headers)
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