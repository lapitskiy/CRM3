# файл удаляется после установки

PLUGIN_CFG_UPDATE = {
    'orders': {
        'nav_url': 'orders_home',
        'nav_name': 'Заказы'
    }
}

INSTALLED_APPS_NAME = 'orders.apps.OrderConfig'

INSTALLED_URL = 'path(\'orders/\', include(\'orders.urls\'))'
#INSTALLED_URL = [
#    path('orders/', include('orders.urls')),
#    ]