import requests

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

# добавляем (оприходуем) товары на мойсклад и обновляем остатки на маркетплейсах
def inventory_moysklad(user, offer_dict):
    headers = get_headers(user)
    update_inventory_moysklad(headers['moysklad_headers'], offer_dict)
    user.replenishment = False
    user.save()

# инвентаризация товара
def update_inventory_moysklad(headers, offer_dict):
    url = 'https://api.moysklad.ru/api/remap/1.2/entity/inventory'
    data = {
        'store': {"meta": get_store_meta(headers)},
        'organization': {'meta': get_organization_meta(headers)},
        'positions': get_inventory_row_data(headers, offer_dict)
    }
    responce = requests.post(url=url, json=data, headers=headers)
    print(f"responce moysklad {responce.json()}")

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