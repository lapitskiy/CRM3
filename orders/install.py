# файл удаляется после установки
MODULE_NAME = 'orders'

INSTALLED_APPS_NAME = 'orders.apps.OrderConfig'

PLUGIN_CFG_UPDATE = {
    'orders': {
        'nav_url': 'orders_home',
        'nav_name': 'Заказы'}}

INSTALLED_URL = {
    'orders': {
        'path': 'orders/',
        'include': 'orders.urls'}}
