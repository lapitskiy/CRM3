


def ms_get_organization_meta_api(headers):
    url = 'https://api.moysklad.ru/api/remap/1.2/entity/organization'
    moysklad_headers = headers.get('moysklad_headers')
    try:
        response = requests.get(url, headers=moysklad_headers)
        if response.status_code == 200:
            response_json = response.json()
            print(f"ms_get_organization_meta (packag): {response_json}")
            exit()
        else:
            result['error'] = response.text
    except Exception as e:
        result['error'] = f"Error in packag request: {e}"
    return response_json['rows'][0]['meta']


def ms_get_agent_meta(headers):
    moysklad_headers = headers.get('moysklad_headers')
    url = 'https://api.moysklad.ru/api/remap/1.2/entity/counterparty/'
    try:
        response = requests.get(url, headers=moysklad_headers)
        if response.status_code == 200:
            response_json = response.json()
            print(f"ms_get_organization_meta (packag): {response_json}")
            exit()
        else:
            result['error'] = response.text
    except Exception as e:
        result['error'] = f"Error in packag request: {e}"
    return response_json['rows'][0]['meta']

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

def ms_create_customerorder(headers: dict):
    result = {}
    moysklad_headers = headers.get('moysklad_headers')
    organization_meta = ms_get_organization_meta(headers)
    agent_meta = ms_get_agent_meta(headers)
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

# получаем последние название оприходвание и списания
async def autoupdate_get_last_sync_acquisition_writeoff_ms(headers: dict):
    result = {}

    moysklad_headers = headers.get('moysklad_headers')
    # оприходование
    url = 'https://api.moysklad.ru/api/remap/1.2/entity/enter'
    params = {
        'limit': 1,
        'order': 'created,desc'
        }
    async with get_http_session() as session:
        async with session.get(url, headers=moysklad_headers, params=params) as response:
            if response.status == 200:
                response_json = await response.json()
                tag = response_json
                print(f"enter: {tag['rows']}")
                result['enter'] = tag['rows'][0]['name']
            else:
                error_message = await response.text()
                result['response'] = error_message
        url = 'https://api.moysklad.ru/api/remap/1.2/entity/loss'
        async with session.get(url, headers=moysklad_headers, params=params) as response:
            if response.status == 200:
                response_json = await response.json()
                tag = response_json
                result['loss'] = tag['rows'][0]['name']
            else:
                error_message = await response.text()
                result['response'] = error_message


    return result