# файл удаляется после установки
MODULE_NAME = 'money'

INSTALLED_APPS_NAME = 'money.apps.MoneyConfig'

PLUGIN_CFG_UPDATE = {
    'money': {
        'nav_url': 'money_home',
        'nav_name': 'Бухгалтерия'}}

INSTALLED_URL = {
    'money': {
        'path': 'money/',
        'include': 'money.urls'}}

def demodata():
    context = 'Данных для установки нет'
    return context
