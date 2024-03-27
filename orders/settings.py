from .models import Category, Status, Device, Service, Category_service
from plugins.models import DesignPosition, DesignRelatedPlugin, Plugins

MODULE_NAME = 'orders'
MODULE_CLASS_NAME = 'Orders'

INSTALLED_APPS_NAME = 'orders.apps.OrderConfig'

PLUGIN_CFG_UPDATE = {
    'orders': {
        'nav_url': 'orders_home',
        'nav_name': 'Заказы'}}

INSTALLED_URL = {
    'orders': {
        'path': 'orders/',
        'include': 'orders.urls'}}

REPO_DATA = {
        'title': 'Заказы',
        'id_in_repo': '',
        'description': '',
        'module_name': 'orders',
        'version': '1',
        'related_class_name': 'Orders'
}

def demodata():
    Category_service.objects.update_or_create(name='Часы')
    # category
    Category.objects.update_or_create(id=1, title='fast', category='fast')
    Category.objects.update_or_create(id=2, title='simple', category='simple')
    # status
    Status.objects.update_or_create(id=1, title='Принято')
    Status.objects.update_or_create(id=2, title='Выдано')
    Status.objects.update_or_create(id=3, title='Отказ')
    # device
    Device.objects.update_or_create(id=1, name='Часы')
    # service
    Service.objects.update_or_create(id=1, name='Мелкий ремонт')
    # DesignPosition
    plugin = Plugins.objects.get(module_name=MODULE_NAME)
    check_plugin = DesignRelatedPlugin.objects.filter(related_plugin=plugin)
    if not check_plugin:
        design_obj = DesignPosition.objects.all()
        for obj in design_obj:
            DesignRelatedPlugin.objects.create(position=obj, related_plugin=plugin)

    context = 'Демо данные установлены'
    return context
