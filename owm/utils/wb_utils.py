import requests
import logging

def wb_update_inventory(headers, stock):
    """
    Обновляет инвентарь на Wildberries.

    Args:
        headers: Словарь с заголовками авторизации.
        stock: Словарь с данными о товарах (vendorCode: {'stock': кол-во, 'sku': sku}).

    Returns:
        Словарь с результатом: {'code': код ответа, 'json': ответ API (JSON или сообщение об успехе/ошибке)}.
        Возвращает ошибку, если произошла ошибка.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        url_cards = 'https://content-api.wildberries.ru/content/v2/get/cards/list'
        url_warehouses = 'https://marketplace-api.wildberries.ru/api/v3/warehouses'
        url_stock = 'https://marketplace-api.wildberries.ru/api/v3/stocks/{warehouseId}'

        data_cards = {
            'settings': {
                'cursor': {'limit': 100, 'nmID': None, 'updatedAt': None},
                'filter': {'withPhoto': -1}
            }
        }
        warehouse_id = None

        while True:  # Внешний цикл обработки страниц
            try:
                response = requests.post(url_cards, json=data_cards, headers=headers['wildberries_headers'])
                response.raise_for_status()  # Проверка статуса ответа
                response_json = response.json()

                # Обработка результата
                for item in response_json['cards']:
                    if item['vendorCode'] in stock:
                        stock[item['vendorCode']]['sku'] = item['sizes'][0]['skus'][0]

                        # Обновление данных для следующей страницы
                if 'cursor' in response_json and response_json['cursor']:
                    data_cards['settings']['cursor']['nmID'] = response_json['cursor']['nmID']
                    data_cards['settings']['cursor']['updatedAt'] = response_json['cursor']['updatedAt']
                else:
                    break  # Выход из цикла, если нет следующей страницы

            except requests.exceptions.RequestException as e:
                logging.error(f"Ошибка при запросе к API: {e}")
                return {'code': 500, 'json': f"Ошибка при запросе к API: {e}"}
            except (KeyError, IndexError) as e:
                logging.error(f"Ошибка при обработке ответа: {e}, данные:{response_json}")
                return {'code': 500, 'json': f"Ошибка при обработке ответа: {e}, данные:{response_json}"}

            if response_json.get('cursor', {}).get('total', 0) < 100:
                break  # Выходим из цикла, если total < 100

        # Получение ID склада
        try:
            warehouse_response = requests.get(url_warehouses, headers=headers['wildberries_headers'])
            warehouse_response.raise_for_status()
            warehouse_data = warehouse_response.json()
            warehouse_id = warehouse_data[0]['id']  # Используем первый элемент списка.
        except requests.exceptions.RequestException as e:
            logging.error(f"Ошибка при получении ID склада: {e}")
            return {'code': 500, 'json': f"Ошибка при получении ID склада: {e}"}


        sku_data = []
        for vendor_code, value in stock.items():
            if 'sku' in value and value.get('stock') is not None:  # Проверяем на None
                try:
                    stock_amount = int(value['stock'])
                    if 0 <= stock_amount <= 100000:  # Проверка на допустимые значения
                        sku_data.append({'sku': value['sku'], 'amount': stock_amount})
                    else:
                        logging.warning(f"Пропущен vendorCode {vendor_code} из-за некорректного значения остатка: {value['stock']}")
                except ValueError as e:
                    logging.error(f"Ошибка при преобразовании остатка {value['stock']} для vendorCode {vendor_code}: {e}")

        if not sku_data:  # Проверка на пустой список
          logging.warning("Список sku_data пуст. Обновление не выполнено.")
          return {"code": 400, "json": "Список sku_data пуст. Обновление не выполнено."}

        # Отправка данных на обновление
        print(f"*" * 100)
        sttt = {'stocks': sku_data}
        print(f"sttt {sttt}")
        print(f"*" * 100)
        try:
            put_response = requests.put(url_stock.format(warehouseId=warehouse_id), json={'stocks': sku_data}, headers=headers['wildberries_headers'])
            print(f'put_response {put_response.text}')
            put_response.raise_for_status()  # проверка
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 409:
                #  В зависимости от вашей логики: повторите запрос через некоторое время, отложите его на потом.
                return {'code': 409, 'json': f"Конфликт при обновлении: {e} {put_response.text}"}
            else:
                logging.error(f"Ошибка при обновлении инвентаря: {e}")
                raise  # Перебросьте исключение вверх
        result = {'code': put_response.status_code, 'json': put_response.json() if put_response.status_code != 204 else 'Обновление прошло успешно'}
        return result
    except Exception as e:
        logging.exception("Непредвиденная ошибка:")
        return {'code': 500, 'json': f"Непредвиденная ошибка: {e}"}