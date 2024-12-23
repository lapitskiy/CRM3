
import requests

from typing import Any, Dict, List

from collections import OrderedDict

# бывший get_moysklad_opt_price
def ms_get_product(headers):
    stock_tuple = {}
    url = "https://api.moysklad.ru/api/remap/1.2/entity/product"
    params = [
        ("limit", 1000)
    ]
    response = requests.get(url, headers=headers, params=params).json()
    return response

def ms_get_organization_meta(headers) -> list:
    result = []
    #url = "https://api.moysklad.ru/api/remap/1.2/entity/metadata?filter=type=organization;type=counterparty"
    url = 'https://api.moysklad.ru/api/remap/1.2/entity/organization/'
    moysklad_headers = headers.get('moysklad_headers')
    try:
        response = requests.get(url, headers=moysklad_headers)
        if response.status_code == 200:
            response_json = response.json()
            result = [{'id': organization['id'], 'name': organization['name']} for organization in response_json['rows']]

                #"href": "https://api.moysklad.ru/api/remap/1.2/entity/group/081922b2-d269-11e4-90a2-8ecb0004410f",
                #"metadataHref": "https://api.moysklad.ru/api/remap/1.2/entity/group/metadata",
        else:
            print(f"error ms_get_organization_meta response.text: {response.text}")
    except Exception as e:
        print(f"error ms_get_organization_meta : {e}")
    return result


def ms_get_agent_meta(headers: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Получает список контрагентов из МойСклад по API.

    :param headers: Словарь с заголовками, включая ключ moysklad_headers.
    :return: Список словарей с полями id и name для каждого контрагента.
    """
    result = []
    moysklad_headers = headers.get('moysklad_headers')

    if not moysklad_headers:
        print("ms_get_agent_meta: moysklad_headers не передан")
        return result

    url = 'https://api.moysklad.ru/api/remap/1.2/entity/counterparty/'
    try:
        response = requests.get(url, headers=moysklad_headers)
        if response.status_code == 200:
            response_json = response.json()
            result = [
                {'id': agent['id'], 'name': agent['name']}
                for agent in response_json['rows']
            ]
            print(f"ms_get_agent_meta (packag): {response_json}")
        else:
            print(f"error ms_get_agent_meta response.text: {response.text}")
    except Exception as e:
        print(f"error ms_get_agent_meta: {e}")
    return result

async def ms_check_customerorder(headers: dict):
    result = {}

    moysklad_headers = headers.get('moysklad_headers')
    # оприходование

    url = 'https://api.moysklad.ru/api/remap/1.2/entity/customerorder'
    params = {
        'limit': 1000,
        'order': 'created,desc'
        }
    async with get_http_session() as session:
        async with session.get(url, headers=moysklad_headers, params=params) as response:
            if response.status == 200:
                response_json = await response.json()
                print(f"customerorder response_json: {response_json}")
            else:
                error_message = await response.text()
                result['response'] = error_message
    return result

def ms_create_customerorder(headers: dict, not_found_product: dict):
    result = {}
    organization_meta = ms_get_organization_meta(headers)
    agent_meta = ms_get_agent_meta(headers)
    moysklad_headers = headers.get('moysklad_headers')
    # оприходование
    url = 'https://api.moysklad.ru/api/remap/1.2/entity/customerorder'
    params = {
         "organization": {'meta': organization_meta},
         "agent": {'meta': agent_meta},
        }
    response = requests.get(url, headers=moysklad_headers, params=params)
    if response.status_code == 200:
        response_json = response.json()
        print(f"response_json META AGENT: {response_json}")
        exit()
    else:
        error_message = response.text
        raise Exception(f"Error {response.status_code}: {error_message}")

    return result

# получаем последние название оприходвание и списания и пишем в базу
def ms_get_last_enterloss(headers: dict):
    result = {}

    moysklad_headers = headers.get('moysklad_headers')
    # оприходование
    url = 'https://api.moysklad.ru/api/remap/1.2/entity/enter'
    params = {
        'limit': 1,
        'order': 'created,desc'
        }
    response = requests.get(url, headers=moysklad_headers, params=params)
    if response.status_code == 200:
        response_json = response.json()
        tag = response_json
        result['enter'] = tag['rows'][0]['name']
    else:
        error_message = response.text
        raise Exception(f"Error {response.status_code}: {error_message}")

    url = 'https://api.moysklad.ru/api/remap/1.2/entity/loss'
    response = requests.get(url, headers=moysklad_headers, params=params)
    if response.status_code == 200:
        response_json = response.json()
        tag = response_json
        result['loss'] = tag['rows'][0]['name']
    else:
        error_message = response.text
        raise Exception(f"Error {response.status_code}: {error_message}")
    return result

# остатки на МС отравляем на все MP
def ms_update_allstock_to_mp(headers):
    '''
    Получаем остатки с МойСклад и выставляем такие же на Озон, Вб, Яндекс
    '''
    from owm.utils.oz_utils import ozon_update_inventory
    from owm.utils.wb_utils import wb_update_inventory
    from owm.utils.ya_utils import yandex_update_inventory

    context = {}
    stock = ms_get_all_stock(headers['moysklad_headers'])
    context['ozon'] = ozon_update_inventory(headers, stock)
    context['yandex'] = yandex_update_inventory(headers, stock)
    context['wb'] = wb_update_inventory(headers, stock)
    return context

def ms_get_all_stock(headers):
    '''
    получаем с МойСклад список всех ОСТАТКОВ
    '''
    stock_tuple = {}
    url = "https://api.moysklad.ru/api/remap/1.2/report/stock/all"
    params = [
        ("filter", "quantityMode=all")
    ]
    response = requests.get(url, headers=headers, params=params).json()
    #print(f'response {response}')
    for stock in response['rows']:
        stock_tuple[stock['article']] = {'stock': int(stock['stock']), 'price' : stock['salePrice']/100 }
    sorted_stock_tuple = OrderedDict(sorted(stock_tuple.items()))
    return sorted_stock_tuple