# файл удаляется после установки
MODULE_NAME = 'goods'
MODULE_CLASS_NAME = 'Goods'

INSTALLED_APPS_NAME = 'goods.apps.GoodsConfig'

PLUGIN_CFG_UPDATE = {
    'goods': {
        'nav_url': 'goods_home',
        'nav_name': 'Товары'}}

INSTALLED_URL = {
    'goods': {
        'path': 'goods/',
        'include': 'goods.urls'}}

REPO_DATA = {
        'title': 'Товары',
        'id_in_repo': '',
        'description': '',
        'module_name': 'goods',
        'version': '1',
        'related_class_name': 'Goods'
}

def demodata():
    context = 'Данных для установки нет'
    return context
