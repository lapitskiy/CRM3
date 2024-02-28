import datetime

import requests
def start(stock_tuple, headers):
    url = 'https://api.partner.market.yandex.ru/campaigns'
    response = requests.get(url, headers=headers).json()
    try:
        for company in response['campaigns']:
            company_id = company['id']
            yandex_get_stocks(company_id, headers, stock_tuple)
    except Exception as ex:
        print(f'Yandex start {ex}')
    return stock_tuple


def update_yandex_stock(company_id, sku, warehouseId, count, headers):
    current_time = datetime.datetime.now()
    offset = datetime.timezone(datetime.timedelta(hours=3))
    formatted_time = current_time.replace(tzinfo=offset).isoformat()
    try:
        url = f'https://api.partner.market.yandex.ru/campaigns/{company_id}/offers/stocks'
        sku = {
            'sku': sku,
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
        requests.put(url=url, data=data, headers=headers)
    except Exception as ex:
        print(f'Yandex update_yandex_stock {ex}')


def yandex_get_stocks(company_id, headers, stock_tuple, pagin=False):
    url = f'https://api.partner.market.yandex.ru/campaigns/{company_id}/offers/stocks'
    data = {
        'archived': False,
    }
    if pagin:
        data['page_token'] = pagin
    response = requests.post(url, headers=headers).json()
    try:
        if response['status'] == 'OK':
            for warehouse in response['result']['warehouses']:
                for offer in warehouse['offers']:
                    for stock in offer['stocks']:
                        if stock['type'] == 'AVAILABLE':
                            if stock['count'] < offer['offerId']:
                                offer['offerId'] = stock['count']
                            else:
                                update_yandex_stock(company_id=company_id, sku=offer['offerId'],
                                                    warehouseId=warehouse['warehouseId'], count=offer['offerId'])
    except Exception as ex:
        print(f'Yandex yandex_get_stocks {ex}')


