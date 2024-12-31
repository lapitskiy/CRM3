import datetime
import os
import requests
import yandex, ozon, wb
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'crm3.settings'
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

from owm.models import Seller


def run():
    while True:
        for user in Seller.objects.all():
            if not user.replenishment:
                a = False
                if user.moysklad_api:
                    moysklad_headers = {
                        "Authorization": f"Bearer {user.moysklad_api}",
                    }
                    stock_tuple = get_all_stock(headers=moysklad_headers)
                if user.yandex_api:
                    yandex_headers = {
                        'Accept': 'application/json',
                        'Authorization': f'Bearer {user.yandex_api}'
                    }
                    yandex.start(stock_tuple=stock_tuple, headers=yandex_headers)
                    a = True
                if user.ozon_api and user.client_id:
                    ozon_headers = {
                        'Client-Id': user.client_id,
                        'Api-Key': user.ozon_api
                    }
                    ozon.start(stock_tuple=stock_tuple, headers=ozon_headers)
                    a = True
                if user.wildberries_api:
                    wildberries_headers = {
                        'Authorization': user.wildberries_api
                    }
                    wb.start(headers=wildberries_headers, stock_tuple=stock_tuple)
                    a = True
                if a and not user.replenishment:
                    last_tuple = get_stock_meta(headers=moysklad_headers)
                    update_all_stock(headers=moysklad_headers, stock_tuple=stock_tuple, last_tuple=last_tuple)

#run()