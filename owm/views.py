import datetime

import requests
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from .models import Parser
from .utils import *
from django.core.exceptions import ObjectDoesNotExist

from datetime import datetime
import locale
import pymorphy2

def get_prod_meta(headers, offer_dict):
    #url = f'https://api.moysklad.ru/api/remap/1.2/entity/assortment?filter=article={article}'
    url = f'https://api.moysklad.ru/api/remap/1.2/entity/assortment'
    response = requests.get(url, headers=headers).json()
    #print(f'get_prod_meta {response[']}')
    data = []
    for row in response['rows']:
        if row['article'] in offer_dict:
            data.append({
                "quantity": float(offer_dict[row['article']]['stock']),
                "price": float(offer_dict[row['article']]['price']) * 100,
                "assortment": {
                    "meta": row['meta']
                },
                "overhead": 0
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

# оприходование товара
def update_enter_moysklad(headers, offer_dict):
    url = 'https://api.moysklad.ru/api/remap/1.2/entity/enter'
    data = {
        'store': {"meta": get_store_meta(headers)},
        'organization': {'meta': get_organization_meta(headers)},
        'positions': get_prod_meta(headers, offer_dict)
    }
    responce = requests.post(url=url, json=data, headers=headers)
    print(f"responce moysklad {responce.json()}")

#обновляет толко остаток
def update_enter_yandex(headers, article, count):
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

def update_enter_ozon(headers, article, count):
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
    #print(response)

def update_enter_wb(headers, article, count):
    url = 'https://suppliers-api.wildberries.ru/content/v2/get/cards/list'
    data = {
        'settings': {
            'cursor': {
                'limit': 1
            },
            'filter': {
                'textSearch': article
            }
        }
    }
    response = requests.post(url, json=data, headers=headers).json()
    #print(response.text)
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

# добавляем (оприходуем) товары на мойсклад и обновляем остатки на маркетплейсах
def enter_moysklad(user, offer_dict):
    headers = get_headers(user)
    update_enter_moysklad(headers['moysklad_headers'], offer_dict)
    # try:
    #     update_stock_moysklad(headers['moysklad_headers'], offer_dict)
    # except Exception as ex:
    #     print(f'update_stock_moysklad {ex}')
    try:
        update_enter_yandex(headers['yandex_headers'], offer_dict)
    except Exception as ex:
        print(f'update_stock_yandex {ex}')
    try:
        update_enter_ozon(headers['ozon_headers'], offer_dict)
    except Exception as ex:
        print(f'update_stock_ozon {ex}')
    try:
        update_enter_wb(headers['wildberries_headers'], offer_dict)
    except Exception as ex:
        print(f'update_stock_wb {ex}')
    user.replenishment = False
    user.save()

# создание dict из POST запроса для Оприходования(enter)
def enter_POST_to_offer_dict(post):
    offer_dict = {}
    for key, value in post.items():
        if value == 'offer_id':
            stock = post[key+'_stock'] # convert float format from ',' to '.'
            if float(stock.replace(',', '.')) == 0:
                continue
            price = post[key+'_price']
            offer_dict[key] = {'stock' : stock.replace(',', '.'), 'price' : price.replace(',', '.')}
    return offer_dict

# создание dict из POST запроса для обновления цены (price)
def price_POST_to_offer_dict(post):
    offer_dict = {}
    for key, value in post.items():
        if value == 'offer_id':
            print(f'post {post}')
            min_price = post[key + '_min_price']
            offer_dict[key] = {'min_price': min_price}
    #print(f"offer_dict {offer_dict}")
    return offer_dict

# оприходование
class Enter(View):
    def get(self, request, *args, **kwargs):
        context = {}
        try:
            parser = Parser.objects.get(user=request.user)
            headers = get_headers(parser)
            stock = get_all_moysklad_stock(headers['moysklad_headers'])
            context['stock'] = stock
        except ObjectDoesNotExist:
            context['error'] = 'нет api'
        #print(f"stock {stock}")
        return render(request, 'owm/enter.html', context)

    def post(self, request):
        #print(f"post {request.POST.dict()}")
        offer_dict = enter_POST_to_offer_dict(request.POST.dict())
        #print(f"offer {offer_dict}")
        #article = request.POST.get('article')
        #count = int(request.POST.get('count'))
        #price = int(request.POST.get('price'))
        parser = Parser.objects.get(user=request.user)
        parser.replenishment = True
        parser.save()
        enter_moysklad(parser, offer_dict)
        #main(parser, article, count, price)
        #main(parser, article, count)
        return HttpResponseRedirect('store')

# инвентаризация c автоматическим оприходованием и списанием
class Inventory(View):
    def get(self, request, *args, **kwargs):
        context = {}
        parser = Parser.objects.get(user=request.user)
        headers = get_headers(parser)
        stock = get_all_moysklad_stock(headers['moysklad_headers'])
        context['stock'] = stock
        #print(f"stock {stock}")
        return render(request, 'owm/inventory.html', context)

    def post(self, request):
        #print(f"post {request.POST.dict()}")
        context = {}
        invent_dict = inventory_POST_to_offer_dict(request.POST.dict())
        parser = Parser.objects.get(user=request.user)
        parser.replenishment = True
        parser.save()
        context['resp'] = inventory_update(parser, invent_dict)
        print(f"responce {context['resp']}")
        return render(request, 'owm/inventory.html', context)

class Create(View):
    def get(self, request, *args, **kwargs):
        api_list_current_user = Parser.objects.filter(user=request.user).first()
        return render(request, 'owm/create.html', {'api_list_current_user': api_list_current_user})

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
            return HttpResponseRedirect('')
        except Exception as ex:
            print('exc ', str(ex))
            return render(request, 'create.html')

class PriceOzon(View):
    def get(self, request, *args, **kwargs):
        context = {}
        parser = Parser.objects.get(user=request.user)
        headers = get_headers(parser)
        price = get_all_price_ozon(headers)
        context['price'] = price #dict(list(price.items())[:1]) # price
        #print(f"stock {stock}")
        return render(request, 'owm/price_ozon.html', context)

    def post(self, request, *args, **kwargs):
        context = {}
        parser = Parser.objects.get(user=request.user)
        offer_dict = price_POST_to_offer_dict(request.POST.dict())
        update_price_ozon(parser, offer_dict)
        return render(request, 'owm/price_ozon.html', context)

class PriceWb(View):
    def get(self, request, *args, **kwargs):
        context = {}
        parser = Parser.objects.get(user=request.user)
        headers = get_headers(parser)
        price = get_all_price_wb(headers)
        context['price'] = price
        #print(f"stock {stock}")
        return render(request, 'owm/price_wb.html', context)

    def post(self, request, *args, **kwargs):
        context = {}
        parser = Parser.objects.get(user=request.user)
        offer_dict = price_POST_to_offer_dict(request.POST.dict())
        update_price_ozon(parser, offer_dict)
        return render(request, 'owm/price_wb.html', context)

class PriceYandex(View):
    def get(self, request, *args, **kwargs):
        context = {}
        parser = Parser.objects.get(user=request.user)
        headers = get_headers(parser)
        price = get_all_price_yandex(headers)
        context['price'] = price
        #print(f"stock {stock}")
        return render(request, 'owm/price_yandex.html', context)

    def post(self, request, *args, **kwargs):
        context = {}
        parser = Parser.objects.get(user=request.user)
        offer_dict = price_POST_to_offer_dict(request.POST.dict())
        update_price_ozon(parser, offer_dict)
        return render(request, 'owm/price_wb.html', context)

class FinanceOzon(View):
    def get(self, request, *args, **kwargs):
        context = {}

        parser = Parser.objects.get(user=request.user)
        headers = get_headers(parser)
        data = get_finance_ozon(headers, period='month')

        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
        start_date = datetime.strptime(data['header_data']['start_date'], '%Y-%m-%d')
        stop_date = datetime.strptime(data['header_data']['stop_date'], '%Y-%m-%d')
        month_name = start_date.strftime('%B')
        morph = pymorphy2.MorphAnalyzer()
        month_nominative = morph.parse(month_name)[0].inflect({'nomn'}).word
        print(month_nominative)  # Выводит: Октябрь
        # Вычисляем разницу в днях
        day_delta = stop_date - start_date

        context['report'] = data['sorted_report']  # dict(list(price.items())[:1]) # price
        context['summed_totals'] = data['summed_totals']  # dict(list(price.items())[:1]) # price
        context['all_totals'] = data['all_totals']
        context['header_data'] = data['header_data']
        context['header_data']['month'] = month_nominative.capitalize()
        context['header_data']['day_delta'] = day_delta.days



        #print(f"headers {context['headers']}")
        print(f"$$$$$$$$$$$$$$$$$")
        print(f"$$$$$$$$$$$$$$$$$")
        print(f"$$$$$$$$$$$$$$$$$")
        #print(f"all_total {all_totals}")

        return render(request, 'owm/finance_ozon.html', context)

    def post(self, request, *args, **kwargs):
        context = {}
        parser = Parser.objects.get(user=request.user)
        offer_dict = price_POST_to_offer_dict(request.POST.dict())
        update_price_ozon(parser, offer_dict)
        return render(request, 'owm/finance_ozon.html', context)