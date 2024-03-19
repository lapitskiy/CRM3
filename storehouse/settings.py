from plugins.models import DesignPosition, DesignRelatedPlugin, Plugins

# файл удаляется после установки
MODULE_NAME = 'storehouse'
MODULE_CLASS_NAME = 'Storehouses'

INSTALLED_APPS_NAME = 'storehouse.apps.StorehouseConfig'

PLUGIN_CFG_UPDATE = {
    'storehouse': {
        'nav_url': 'storehouse_home',
        'nav_name': 'Склад'}}

INSTALLED_URL = {
    'storehouse': {
        'path': 'storehouse/',
        'include': 'storehouse.urls'}}

REPO_DATA = {
        'title': 'Склады',
        'id_in_repo': '',
        'description': '',
        'module_name': 'storehouse',
        'version': '1',
        'related_class_name': 'StoreRelated'
        }

def demodata():
    # DesignPosition
    plugin = Plugins.objects.get(module_name=MODULE_NAME)
    check_plugin = DesignRelatedPlugin.objects.filter(related_plugin=plugin)
    if not check_plugin:
        design_obj = DesignPosition.objects.all()
        for obj in design_obj:
            DesignRelatedPlugin.objects.create(position=obj, related_plugin=plugin)
    context = 'Данных для установки нет'
    return context