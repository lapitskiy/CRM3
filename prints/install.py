# файл удаляется после установки
MODULE_NAME = 'prints'

INSTALLED_APPS_NAME = 'prints.apps.PrintConfig'

PLUGIN_CFG_UPDATE = {
    'prints': {
        'nav_url': 'prints_home',
        'nav_name': 'Печать'}}

INSTALLED_URL = {
    'prints': {
        'path': 'prints/',
        'include': 'prints.urls'}}

def demodata():
    context = 'Данных для установки нет'
    return context