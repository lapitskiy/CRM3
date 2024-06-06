# файл удаляется после установки
MODULE_NAME = 'clients'
MODULE_CLASS_NAME = 'Clients'

INSTALLED_APPS_NAME = 'clients.apps.ClientConfig'

PLUGIN_CFG_UPDATE = {
    'clients': {
        'nav_url': 'clients_home',
        'nav_name': 'Клиенты'}}

INSTALLED_URL = {
    'clients': {
        'path': 'clients/',
        'include': 'clients.urls'}}

REPO_DATA = {
        'title': 'Клиенты',
        'id_in_repo': '',
        'description': '',
        'module_name': 'clients',
        'version': '1',
        'related_class_name': 'Clients'
}

def demodata():
    context = 'Данных для установки нет'
    return context