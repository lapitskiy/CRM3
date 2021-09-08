# файл удаляется после установки
MODULE_NAME = 'storehouse'

INSTALLED_APPS_NAME = 'storehouse.apps.StorehouseConfig'

PLUGIN_CFG_UPDATE = {
    'storehouse': {
        'nav_url': 'storehouse_home',
        'nav_name': 'Склад'}}

INSTALLED_URL = {
    'storehouse': {
        'path': 'storehouse/',
        'include': 'storehouse.urls'}}

def demodata():
    context = 'Данных для установки нет'
    return context