# CRM3 GLOBAL PLUGINS VARS
REPO_URL = 'http://127.0.0.1:8001/plugins/api/?format=json'
INSTALLED_APPS_ADD = ['plugins.apps.PluginsConfig', 'orders.apps.OrderConfig']
PLUGIN_URLS = {'orders': {'path': 'orders/', 'include': 'orders.urls'}}
PLUGIN_CFG = {'orders': {'nav_url': 'orders_home', 'nav_name': 'Заказы'}}

from .models import Orders, Category, Status, Service

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

def demodata():
    Category.objects.update_or_create(id=1, title='fast')
    Category.objects.update_or_create(id=2, title='simple')
    Status.objects.update_or_create(id=1, title='Принято')
    Status.objects.update_or_create(id=2, title='Выдано')
    Status.objects.update_or_create(id=3, title='Отказ')
