from .models import Category, Status, Device, Service

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
    # category
    Category.objects.update_or_create(id=1, title='fast', category='fast')
    Category.objects.update_or_create(id=2, title='simple', category='simple')
    # status
    Status.objects.update_or_create(id=1, title='Принято')
    Status.objects.update_or_create(id=2, title='Выдано')
    Status.objects.update_or_create(id=3, title='Отказ')
    # device
    Device.objects.update_or_create(id=1, name='Casio')
    # service
    Service.objects.update_or_create(id=1, name='Мелкий ремонт')
    context = 'Демо данные установлены'
    return context
