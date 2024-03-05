import datetime

import requests
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from .models import Parser


def get_organization_meta(headers):
    url = 'https://api.moysklad.ru/api/remap/1.2/entity/organization'
    response = requests.get(url, headers=headers).json()
    return response['rows'][0]['meta']


def get_store_meta(headers):
    url = 'https://api.moysklad.ru/api/remap/1.2/entity/store'
    response = requests.get(url, headers=headers).json()
    return response['rows'][0]['meta']


def get_prod_meta(headers, article, count, price):
    url = f'https://api.moysklad.ru/api/remap/1.2/entity/assortment?filter=article={article}'
    response = requests.get(url, headers=headers).json()
    meta = response['rows'][0]['meta']
    data = [
        {
            "quantity": count,
            "price": price * 100,
            "assortment": {
                "meta": meta
            },
            "overhead": 0
        },
    ]
    return data


def update_stock_moysklad(headers, article, count, price):
    url = 'https://api.moysklad.ru/api/remap/1.2/entity/enter'
    data = {
        'store': {"meta": get_store_meta(headers)},
        'organization': {'meta': get_organization_meta(headers)},
        'positions': get_prod_meta(headers, article, count, price)
    }
    responce = requests.post(url=url, json=data, headers=headers)


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


def update_stock_yandex(headers, article, count):
    url = 'https://api.partner.market.yandex.ru/campaigns'
    response = requests.get(url, headers=headers).json()
    company_id = response['campaigns'][0]['id']
    businessId = response['campaigns'][0]['business']['id']
    url = f'https://api.partner.market.yandex.ru/businesses/{businessId}/warehouses'
    response = requests.get(url, headers=headers).json()
    warehouseId = response['result']['warehouses'][0]['id']
    url = f'https://api.partner.market.yandex.ru/campaigns/{company_id}/stats/skus'
    data = {
        'shopSkus': [article]
    }
    response = requests.post(url, headers=headers, json=data).json()
    for i in response['result']['shopSkus'][0]['warehouses'][0]['stocks']:
        if i['type'] == 'FIT':
            count += i['count']
            break
    current_time = datetime.datetime.now()
    offset = datetime.timezone(datetime.timedelta(hours=3))  # Указываем смещение +03:00
    formatted_time = current_time.replace(tzinfo=offset).isoformat()
    url = f'https://api.partner.market.yandex.ru/campaigns/{company_id}/offers/stocks'
    sku = {
        'sku': article,
        'warehouseId': warehouseId,
        'items': [{
            'count': count,
            'type': 'FIT',
            'updatedAt': formatted_time
        }]
    }
    data = {
        'skus': [sku]
    }
    requests.put(url=url, json=data, headers=headers).json()


def update_stock_ozon(headers, article, count):
    url = 'https://api-seller.ozon.ru/v3/product/info/stocks'
    data = {
        'filter': {
            'offer_id': [article]
        },
        "limit": 1
    }
    response = requests.post(url, json=data, headers=headers).json()
    for i in response['result']['items'][0]['stocks']:
        if i['type'] == 'fbs':
            count += i['present']
            break
    url = 'https://api-seller.ozon.ru/v1/product/import/stocks'
    stocks = [
        {
            'offer_id': article,
            'stock': count
        }
    ]
    data = {
        'stocks': stocks
    }
    requests.post(url, headers=headers, json=data).json()
    print(response)


def update_stock_wb(headers, article, count):
    url = 'https://suppliers-api.wildberries.ru/content/v2/get/cards/list'
    data = {
        'settings': {
            'filter': {
                'textSearch': article
            }
        }
    }
    response = requests.post(url, json=data, headers=headers).json()
    print(response.text)
    barcode = response['cards'][0]['sizes'][0]['skus'][0]
    url = 'https://suppliers-api.wildberries.ru/api/v3/warehouses'
    response = requests.get(url, headers=headers).json()
    warehouseId = response[0]['id']
    url = f'https://suppliers-api.wildberries.ru/api/v3/stocks/{warehouseId}'
    data = {
        'skus': [barcode]
    }
    response = requests.post(url, json=data, headers=headers).json()
    count += response['stocks'][0]['amount']
    url = f'https://suppliers-api.wildberries.ru/api/v3/stocks/{warehouseId}'
    data = {
        'stocks': [
            {
                'sku': barcode,
                'amount': count
            }
        ]
    }
    response = requests.put(url, json=data, headers=headers)


def main(user, article, count, price):
    headers = get_headers(user)
    try:
        update_stock_moysklad(headers['moysklad_headers'], article, count, price)
    except Exception as ex:
        print(f'update_stock_moysklad {ex}')
    try:
        update_stock_yandex(headers['yandex_headers'], article, count)
    except Exception as ex:
        print(f'update_stock_yandex {ex}')
    try:
        update_stock_ozon(headers['ozon_headers'], article, count)
    except Exception as ex:
        print(f'update_stock_ozon {ex}')
    try:
        update_stock_wb(headers['wildberries_headers'], article, count)
    except Exception as ex:
        print(f'update_stock_wb {ex}')
    user.replenishment = False
    user.save()

def get_all_moysklad_stock(headers):
    stock_tuple = {}
    url = "https://api.moysklad.ru/api/remap/1.2/report/stock/all"
    response = requests.get(url, headers=headers).json()
    for stock in response['rows']:
        stock_tuple[stock['article']] = stock['stock']
    return stock_tuple

class Store(View):
    def get(self, request, *args, **kwargs):
        context = {}
        parser = Parser.objects.get(user=request.user)
        headers = get_headers(parser)
        stock = get_all_moysklad_stock(headers['moysklad_headers'])
        context['stock'] = stock
        print(f"stock {stock}")
        return render(request, 'store.html', context)

    def post(self, request):
        article = request.POST.get('article')
        count = int(request.POST.get('count'))
        price = int(request.POST.get('price'))
        parser = Parser.objects.get(user=request.user)
        parser.replenishment = True
        parser.save()
        main(parser, article, count, price)
        return HttpResponseRedirect('store')

class Create(View):
    def get(self, request, *args, **kwargs):
        api_list_current_user = Parser.objects.filter(user=request.user).first()
        return render(request, 'create.html', {'api_list_current_user': api_list_current_user})

    def post(self, request, *args, **kwargs):
        try:
            moysklad_api = request.POST.get('moysklad_api')
            yandex_api = request.POST.get('yandex_api')
            wildberries_api = request.POST.get('wildberries_api')
            client_id = request.POST.get('client_id')
            ozon_api = request.POST.get('ozon_api')
            print('moysklad_api ', moysklad_api)
            print('ozon_api ', ozon_api)
            print('curr user ', request.user)
            user_api_object = Parser.objects.filter(user=request.user)
            if user_api_object:
                user_api_object.update(
                    moysklad_api=moysklad_api,
                    yandex_api=yandex_api,
                    wildberries_api=wildberries_api,
                    client_id=client_id,
                    ozon_api=ozon_api,
                )
            else:
                Parser.objects.update_or_create(
                    user=request.user,
                    moysklad_api=moysklad_api,
                    yandex_api=yandex_api,
                    wildberries_api=wildberries_api,
                    client_id=client_id,
                    ozon_api=ozon_api,
                )
            return HttpResponseRedirect('store')
        except Exception as ex:
            print('exc ', str(ex))
            return render(request, 'create.html')