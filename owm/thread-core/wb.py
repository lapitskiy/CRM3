import requests
def update_stock(warehouseId, stocks, headers):
    url = f'https://suppliers-api.wildberries.ru/api/v3/stocks/{warehouseId}'
    last_i = 0
    for i in range(1000, len(stocks)+1000, 1000):
        try:
            data = {'stocks': stocks[last_i:i]}
            requests.put(url, data=data, headers=headers)
            last_i = i
        except Exception as ex:
            print(f'Wb update_stock {ex}')
def get_stocks(barcodes, stock_tuple, headers, warehouseId):
    url = f'https://suppliers-api.wildberries.ru/api/v3/stocks/{warehouseId}'
    last_i = 0
    stocks = []
    for i in range(1000, len(barcodes) + 1000, 1000):
        try:
            response = requests.post(url=url, headers=headers, data=barcodes[last_i: i]).json()
            for stock in response['stocks']:
                if stock['amount'] <= stock_tuple[stock['sku']]:
                    stock_tuple[stock['sku']] = stock['amount']
                else:
                    stocks.append({
                        'sku': stock['sku'],
                        'amount': stock_tuple[stock['sku']]
                    })
            last_i = i
        except Exception as ex:
            print(f'Wb get_stock {ex}')
    update_stock(warehouseId, stocks, headers)
    return stock_tuple


def get_prods(headers, warehouseId, stock_tuple):
    barcodes = []
    barcodes_tuple = {}
    data = {
        "settings": {
            "cursor": {
                "limit": 1000
            },
            "filter": {
                "withPhoto": -1
            }
        }
    }
    url = f'https://suppliers-api.wildberries.ru/api/v3/stocks/{warehouseId}'
    while True:
        try:
            responce = requests.post(url=url, headers=headers, data=data).json()
            for i in responce['cards']:
                barcodes.append(i['sizes'][0]['skus'][0])
                barcodes_tuple[i['sizes'][0]['skus'][0]] = i['vendorCode']
            if responce['cursor']['total'] < 1000:
                break
            data['cursor']['updatedAt'] = responce['cursor']['updatedAt']
            data['cursor']['nmID'] = responce['cursor']['nmID']
        except Exception as ex:
            print(f'Wb get_prods {ex}')
            break
    get_stocks(barcodes, stock_tuple, headers, warehouseId)
    return stock_tuple


def start(headers, stock_tuple):
    url = 'https://suppliers-api.wildberries.ru/api/v3/warehouses'
    responce = requests.get(url=url, headers=headers).json()
    for i in responce:
        try:
            get_prods(headers, i['id'], stock_tuple)
        except Exception as ex:
            print(f'Wb start {ex}')
    return stock_tuple
