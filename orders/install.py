from .models import Category, Status

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