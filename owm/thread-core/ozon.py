import requests

def update_stock(stocks, headers):
    try:
        url = 'https://api-seller.ozon.ru/v1/product/import/stocks'
        last_i = 0
        #if not stocks:
        #    stocks = ['',]
        for i in range(80, len(stocks)+80, 80):
            data = {'stocks': stocks[last_i:stocks]}
            requests.post(url, json=data, headers=headers)
            last_i = i
    except Exception as ex:
        print(f'Ozon update_stock {ex}')
        print(f'Ozon last_i {last_i}')
        #print(f'data {data}')
        print(f'stock {len(stocks)}')
        print(f'stock {stocks}')
        print(f'stock last_i {stocks[0:stocks]}')


def check_stock(response, stock_tuple, headers, stocks):
    for prod in response:
        try:
            offer_id = prod['offer_id']
            if prod['stocks']['present'] < stock_tuple[offer_id]:
                print(f"{prod['stocks']['present']} - {stock_tuple[offer_id]}")
                stock_tuple[offer_id] = prod['stocks']['present']
            else:
                stocks.append(
                    {
                        'offer_id': offer_id,
                        'product_id': prod['id'],
                        'stock': prod['stocks']['present']
                     }
                )
        except Exception as ex:
            print(f'Ozon check_stock {ex}')
    update_stock(stocks, headers)
    return stock_tuple


def start(stock_tuple, headers):
    try:
        print('start ozon')
        a = [i for i in stock_tuple] # получаем артикулы в list
        stocks = []
        url = 'https://api-seller.ozon.ru/v2/product/info/list'
        last_i = 0
        for i in range(1000, len(a)+1000, 1000): # ограничение на 1000 позиций в запросе
            data = {
                'offer_id': a[last_i:i]
            }
            response = requests.post(url, headers=headers, json=data).json()
            #print(f'response ozon {response}')
            #print(f'stock {stocks}')
            check_stock(response['result']['items'], stock_tuple, headers, stocks)
            last_i = i
        #update_stock(stocks, headers)
    except Exception as ex:
        print(f'Ozon start {ex}')
    return stock_tuple


