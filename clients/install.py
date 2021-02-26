# файл удаляется после установки
MODULE_NAME = 'clients'

INSTALLED_APPS_NAME = 'clients.apps.ClientConfig'

PLUGIN_CFG_UPDATE = {
    'clients': {
        'nav_url': 'clients_home',
        'nav_name': 'Клиенты'}}

INSTALLED_URL = {
    'clients': {
        'path': 'clients/',
        'include': 'clients.urls'}}

def demodata():
    context = 'Данных для установки нет'
    return context