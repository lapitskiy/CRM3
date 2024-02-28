import datetime
import os

import requests
import yandex, ozon, wb
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'djangoProject2.settings'
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()
from app.models import Parser


def update_all_stock(headers, stock_tuple, last_tuple):
    positions = []
    url = 'https://api.moysklad.ru/api/remap/1.2/entity/loss'
    for i in stock_tuple:
        try:
            if stock_tuple[i] < last_tuple[i]:
                positions.append(
                    {
                        'quantity': last_tuple[i]['stock'] - stock_tuple[i],
                        'assortment': {'meta': last_tuple[i]['meta']}
                    }
                )
        except Exception as ex:
            print(f'main update_all_stock {ex}')
    data = {
        'store': {"meta": get_store_meta(headers)},
        'organization': {'meta': get_organization_meta(headers)},
        'positions': positions
    }
    requests.post(url=url, headers=headers, json=data)


def get_organization_meta(headers):
    url = 'https://api.moysklad.ru/api/remap/1.2/entity/organization'
    response = requests.get(url, headers=headers).json()
    return response['rows'][0]['meta']


def get_store_meta(headers):
    url = 'https://api.moysklad.ru/api/remap/1.2/entity/store'
    response = requests.get(url, headers=headers).json()
    return response['rows'][0]['meta']


def get_stock_meta(headers):
    last_tuple = {}
    url = "https://api.moysklad.ru/api/remap/1.2/report/stock/all"
    response = requests.get(url, headers=headers)
    for stock in response['rows']:
        last_tuple[stock['article']] = {
            'meta': stock['meta'],
            'stock': stock['stock']
        }
    return last_tuple


def get_all_stock(headers):
    stock_tuple = {}
    url = "https://api.moysklad.ru/api/remap/1.2/report/stock/all"
    response = requests.get(url, headers=headers)
    for stock in response['rows']:
        stock_tuple[stock['article']] = stock['stock']
    return stock_tuple


def run():
    while True:
        for user in Parser.objects.all():
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

run()