import datetime

import requests
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from .models import Seller, Crontab
from owm.utils.base_utils import get_headers, base_get_metadata
from django.core.exceptions import ObjectDoesNotExist

from django.http import HttpResponse

from datetime import datetime

from .utils.db_utils import db_update_metadata
from .utils.ms_utils import ms_update_allstock_to_mp, ms_get_last_enterloss
from .utils.oz_utils import ozon_get_finance


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
    async def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # или другая страница
        context = {}
        try:
            parser = Seller.objects.get(user=request.user)
            headers = await get_headers(parser_data)
            stock = get_all_moysklad_stock(headers['moysklad_headers'])
            context['stock'] = stock
        except ObjectDoesNotExist:
            context['error'] = 'нет api'
        #print(f"stock {stock}")
        return render(request, 'owm/enter.html', context)

    async def post(self, request):
        #print(f"post {request.POST.dict()}")
        offer_dict = enter_POST_to_offer_dict(request.POST.dict())
        #print(f"offer {offer_dict}")
        #article = request.POST.get('article')
        #count = int(request.POST.get('count'))
        #price = int(request.POST.get('price'))
        parser = Seller.objects.get(user=request.user)
        parser.replenishment = True
        parser.save()
        enter_moysklad(parser, offer_dict)
        #main(parser, article, count, price)
        #main(parser, article, count)
        return HttpResponseRedirect('store')

# инвентаризация c автоматическим оприходованием и списанием
class Inventory(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # или другая страница
        context = {}
        parser = Seller.objects.get(user=request.user)
        headers = get_headers(parser)
        stock = get_all_moysklad_stock(headers['moysklad_headers'])
        context['stock'] = stock
        #print(f"stock {stock}")
        return render(request, 'owm/inventory.html', context)

    def post(self, request):
        #print(f"post {request.POST.dict()}")
        context = {}
        invent_dict = inventory_POST_to_offer_dict(request.POST.dict())
        user = Seller.objects.get(user=request.user)
        context['resp'] = inventory_update(user, invent_dict)
        print(f"context resp {context['resp']}")
        return render(request, 'owm/inventory.html', context)

class Autoupdate(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # или другая страница
        context = {}
        parser = Seller.objects.get(user=request.user)
        headers = get_headers(parser)
        autoupdate_get_last_sync_acquisition_writeoff_ms(headers)
        #stock = auto_update_owm_moysklad(headers['moysklad_headers'])
        context['stock'] = stock
        #print(f"stock {stock}")
        return render(request, 'owm/autoupdate.html', context)

    def post(self, request):
        #print(f"post {request.POST.dict()}")
        context = {}
        invent_dict = inventory_POST_to_offer_dict(request.POST.dict())
        parser = Seller.objects.get(user=request.user)
        context['resp'] = inventory_update(parser, invent_dict)
        print(f"responce {context['resp']}")
        return render(request, 'owm/autoupdate.html', context)

class AutoupdateSettings(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # или другая страница
        context = {}
        try:
            obj = Crontab.objects.get(seller__user=request.user, name='autoupdate')
            context['active'] = obj.active
            context['active_yandex'] = obj.yandex
            context['active_ozon'] = obj.ozon
            context['active_wb'] = obj.wb

            parser = obj.seller

            parser_data = {
                'moysklad_api': parser.moysklad_api,
                'yandex_api': parser.yandex_api,
                'wildberries_api': parser.wildberries_api,
                'ozon_api': parser.ozon_api,
                'ozon_id': parser.client_id,
            }

            try:
                headers = get_headers(parser_data)
            except Exception as e:
                print("Error occurred:", e)


            cron_data = {
                'cron_dict': obj.crontab_dict,
            }

            #await autoupdate_get_last_sync_acquisition_writeoff_ms(headers=headers)

        except Crontab.DoesNotExist:
            user = Seller.objects.get(user=request.user)
            Crontab.objects.create(seller=user, name='autoupdate', active=False)

            print(f"Created new Crontab")
        return render(request, 'owm/autoupdate/autoupdate_settings.html', context)

    def post(self, request):
        context = {}

        form_type = request.POST.get("form_type")
        crontab = Crontab.objects.get(seller__user=request.user, name='autoupdate')

        if form_type == "save_settings":
            sync_checkbox = request.POST.get('sync_checkbox', False)
            sync_checkbox_ozon = request.POST.get('sync_checkbox_ozon', False)
            sync_checkbox_yandex = request.POST.get('sync_checkbox_yandex', False)
            sync_checkbox_wb = request.POST.get('sync_checkbox_wb', False)



            if sync_checkbox == 'on':
                crontab.active = True
                context['active'] = True
                print("Checkbox is checked")
            else:
                crontab.active = False
                context['active'] = False
                # Чекбокс не отмечен
                print("Checkbox is not checked")

            if sync_checkbox_ozon == 'on':
                crontab.ozon = True
                context['active_ozon'] = True
            else:
                crontab.ozon = False
                context['active_ozon'] = False

            if sync_checkbox_yandex == 'on':
                crontab.yandex = True
                context['active_yandex'] = True
            else:
                crontab.yandex = False
                context['active_ozon'] = False

            if sync_checkbox_wb == 'on':
                crontab.wb = True
                context['active_wb'] = True
            else:
                crontab.wb = False
                context['active_wb'] = False
            crontab.save()

        elif form_type == "sync_start":
            parser = crontab.seller  # Асинхронный доступ к связанному объекту
            parser_data = {
                'moysklad_api': parser.moysklad_api,
                'yandex_api': parser.yandex_api,
                'wildberries_api': parser.wildberries_api,
                'ozon_api': parser.ozon_api,
                'ozon_id': parser.client_id,
            }
            try:
                headers = get_headers(parser_data)
            except Exception as e:
                print("Error occurred:", e)
            context['update_data'] = ms_update_allstock_to_mp(headers=headers)
            print(f"update_data", context['update_data'])
            codes = [context['update_data']['wb']['code'], context['update_data']['wb']['code'], context['update_data']['yandex']['code']]
            # Проверка, все ли значения равны 200 или 204
            if all(code in (200, 204, 409) for code in codes):
                result_dict = ms_get_last_enterloss(headers=headers)
                crontab.crontab_dict = result_dict
                crontab.save()
        context['sync_update'] = True
        return render(request, 'owm/autoupdate_settings.html', context)

class SettingsApi(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # или другая страница
        api_list_current_user = Seller.objects.filter(user=request.user).first()
        return render(request, 'owm/settings/settings_api.html', {'api_list_current_user': api_list_current_user})

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
            user_api_object = Seller.objects.filter(user=request.user)
            if user_api_object:
                user_api_object.update(
                    moysklad_api=moysklad_api,
                    yandex_api=yandex_api,
                    wildberries_api=wildberries_api,
                    client_id=client_id,
                    ozon_api=ozon_api,
                )
            else:
                Seller.objects.update_or_create(
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
            return render(request, 'owm/settings/settings_api.html')

class SettingsContragent(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # или другая страница
        context = {}

        seller = Seller.objects.get(user=request.user)

        parser_data = {
            'moysklad_api': seller.moysklad_api,
            'yandex_api': seller.yandex_api,
            'wildberries_api': seller.wildberries_api,
            'ozon_api': seller.ozon_api,
            'ozon_id': seller.client_id,
        }

        headers = get_headers(parser_data)

        metadata = base_get_metadata(headers=headers, seller=seller.id)

        for key in metadata.items():
            print(f"key {key}")
            if 'db' in key:
                context[key] = metadata[key]['db']
        context['agentlist'] = metadata['agentlist']
        context['orglist'] = metadata['orglist']
        #print(f"context {context['contragent']}")
        return render(request, 'owm/settings/settings_contragent.html', context)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # или другая страница
        context = {}
        metadata={}
        metadata['organization'] = request.POST.get('organization_select')
        metadata['wb'] = request.POST.get('wb_select')
        metadata['ozon'] = request.POST.get('ozon_select')
        metadata['yandex'] = request.POST.get('yandex_select')

        seller = Seller.objects.get(user=request.user)

        db_update_metadata(seller=seller, metadata=metadata)

        return redirect('settings_contragent')  # или другая страница



class PriceOzon(View):
    def get(self, request, *args, **kwargs):
        context = {}
        parser = Seller.objects.get(user=request.user)
        headers = get_headers(parser)
        price = get_all_price_ozon(headers)
        context['price'] = price #dict(list(price.items())[:1]) # price
        #print(f"stock {stock}")
        return render(request, 'owm/price_ozon.html', context)

    def post(self, request, *args, **kwargs):
        context = {}
        parser = Seller.objects.get(user=request.user)
        offer_dict = price_POST_to_offer_dict(request.POST.dict())
        update_price_ozon(parser, offer_dict)
        return render(request, 'owm/price_ozon.html', context)

class PriceWb(View):
    def get(self, request, *args, **kwargs):
        context = {}
        parser = Seller.objects.get(user=request.user)
        headers = get_headers(parser)
        price = get_all_price_wb(headers)
        context['price'] = price
        #print(f"stock {stock}")
        return render(request, 'owm/price_wb.html', context)

    def post(self, request, *args, **kwargs):
        context = {}
        parser = Seller.objects.get(user=request.user)
        offer_dict = price_POST_to_offer_dict(request.POST.dict())
        update_price_ozon(parser, offer_dict)
        return render(request, 'owm/price_wb.html', context)

class PriceYandex(View):
    def get(self, request, *args, **kwargs):
        context = {}
        parser = Seller.objects.get(user=request.user)
        headers = get_headers(parser)
        price = get_all_price_yandex(headers)
        context['price'] = price
        #print(f"stock {stock}")
        return render(request, 'owm/price_yandex.html', context)

    def post(self, request, *args, **kwargs):
        context = {}
        parser = Seller.objects.get(user=request.user)
        offer_dict = price_POST_to_offer_dict(request.POST.dict())
        update_price_ozon(parser, offer_dict)
        return render(request, 'owm/price_wb.html', context)

class FinanceOzon(View):
    def get(self, request, *args, **kwargs):
        context = {}

        parser = Seller.objects.get(user=request.user)
        parser_data = {
            'moysklad_api': parser.moysklad_api,
            'yandex_api': parser.yandex_api,
            'wildberries_api': parser.wildberries_api,
            'ozon_api': parser.ozon_api,
            'ozon_id': parser.client_id,
        }
        headers = get_headers(parser_data)
        data = ozon_get_finance(headers, period='month')

        context['report'] = data['sorted_report']  # dict(list(price.items())[:1]) # price
        context['summed_totals'] = data['summed_totals']  # dict(list(price.items())[:1]) # price
        context['all_totals'] = data['all_totals']
        context['header_data'] = data['header_data']

        #print(f"headers {context['headers']}")
        print(f"$$$$$$$$$$$$$$$$$")
        print(f"$$$$$$$$$$$$$$$$$")
        print(f"$$$$$$$$$$$$$$$$$")
        #print(f"all_total {all_totals}")

        return render(request, 'owm/finance_ozon.html', context)

    def post(self, request, *args, **kwargs):
        context = {}
        parser = Seller.objects.get(user=request.user)
        offer_dict = price_POST_to_offer_dict(request.POST.dict())
        update_price_ozon(parser, offer_dict)
        return render(request, 'owm/finance_ozon.html', context)

class PostavkaOzon(View):
    def get(self, request, *args, **kwargs):
        context = {}
        parser = Seller.objects.get(user=request.user)
        headers = get_headers(parser)
        data = get_postavka_ozon(headers)
        # print(f"headers {context['headers']}")
        # print(f"all_total {all_totals}")
        context['row'] = data['row']
        context['path'] = data['path']
        context['code'] = data['code']
        return render(request, 'owm/postavka_ozon.html', context)

    def post(self, request, *args, **kwargs):
        context = {}
        parser = Seller.objects.get(user=request.user)
        offer_dict = price_POST_to_offer_dict(request.POST.dict())
        update_price_ozon(parser, offer_dict)
        return render(request, 'owm/finance_ozon.html', context)

class OtpravlenieOzon(View):
    async def get(self, request, *args, **kwargs):
        context = {}
        try:
            context = {}
            parser = await sync_to_async(Seller.objects.get)(user=request.user)
            parser_data = {
                'moysklad_api': parser.moysklad_api,
                'yandex_api': parser.yandex_api,
                'wildberries_api': parser.wildberries_api,
                'ozon_api': parser.ozon_api,
                'ozon_id': parser.client_id,
            }

            headers = await get_headers(parser_data)

            result = await get_otpravlenie_ozon(headers)

            context['otpravlenie'] = result['awaiting']
            context['packag'] = result['packag']
        except ObjectDoesNotExist:
            context['error'] = 'нет api'
        return await sync_to_async(render)(request, 'owm/otpravlenie_ozon.html', context)

    async def post(self, request):
        context = {}

        form_type = request.POST.get("form_type")
        crontab = await sync_to_async(Crontab.objects.get)(seller__user=request.user, name='autoupdate')

        if form_type == "save_settings":
            sync_checkbox = request.POST.get('sync_checkbox', False)
            sync_checkbox_ozon = request.POST.get('sync_checkbox_ozon', False)
            sync_checkbox_yandex = request.POST.get('sync_checkbox_yandex', False)
            sync_checkbox_wb = request.POST.get('sync_checkbox_wb', False)



            if sync_checkbox == 'on':
                crontab.active = True
                context['active'] = True
                print("Checkbox is checked")
            else:
                crontab.active = False
                context['active'] = False
                # Чекбокс не отмечен
                print("Checkbox is not checked")

            if sync_checkbox_ozon == 'on':
                crontab.ozon = True
                context['active_ozon'] = True
            else:
                crontab.ozon = False
                context['active_ozon'] = False

            if sync_checkbox_yandex == 'on':
                crontab.yandex = True
                context['active_yandex'] = True
            else:
                crontab.yandex = False
                context['active_ozon'] = False

            if sync_checkbox_wb == 'on':
                crontab.wb = True
                context['active_wb'] = True
            else:
                crontab.wb = False
                context['active_wb'] = False
            crontab.save()

        elif form_type == "sync_start":
            mp_reserv = request.POST.get('mp_reserv', False)
            if mp_reserv == 'on':
                reserv_dict = get_reserv_from_mp(headers=headers)
            else:
                #print('tyt')
                #parser = Parser.objects.get(user=request.user)
                parser = await sync_to_async(lambda: crontab.seller)()  # Асинхронный доступ к связанному объекту

                parser_data = {
                    'moysklad_api': parser.moysklad_api,
                    'yandex_api': parser.yandex_api,
                    'wildberries_api': parser.wildberries_api,
                    'ozon_api': parser.ozon_api,
                    'ozon_id': parser.client_id,
                }
                try:
                    headers = await get_headers(parser_data)
                except Exception as e:
                    print("Error occurred:", e)
                context['update_data'] = update_stock_mp_from_ms(headers=headers)

                codes = [context['update_data']['wb']['code'], context['update_data']['wb']['code'], context['update_data']['yandex']['code']]
                # Проверка, все ли значения равны 200 или 204
                if all(code in (200, 204) for code in codes):
                    context['sync_update'] = True
                    result_dict = await autoupdate_get_last_sync_acquisition_writeoff_ms(headers=headers)
                    crontab.crontab_dict = result_dict
                    await sync_to_async(crontab.save)()


        return await sync_to_async(render)(request, 'owm/autoupdate_settings.html', context)

class FinanceWb(View):
    def get(self, request, *args, **kwargs):
        context = {}
        try:
            parser = Seller.objects.get(user=request.user)
            # дальнейшая логика
        except TypeError:
            return HttpResponse('Пользователь не аутентифицирован', status=401)

        headers = get_headers(parser)
        data = get_finance_wb(headers, period='month')
        context['path'] = data['path']
        context['code'] = data['code']
        context['date'] = data['date']
        context['report'] = data['sorted_report']  # dict(list(price.items())[:1]) # price
        context['summed_totals'] = data['summed_totals']  # dict(list(price.items())[:1]) # price
        context['all_totals'] = data['all_totals']
        #print(f"headers {context['headers']}")
        print(f"$$$$$$$$$$$$$$$$$")
        #print(f"all_total {all_totals}")

        return render(request, 'owm/finance_wb.html', context)

    def post(self, request, *args, **kwargs):
        context = {}
        parser = Seller.objects.get(user=request.user)
        offer_dict = price_POST_to_offer_dict(request.POST.dict())
        update_price_ozon(parser, offer_dict)
        return render(request, 'owm/finance_ozon.html', context)
