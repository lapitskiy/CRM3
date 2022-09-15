# файл удаляется после установки
MODULE_NAME = 'money'
MODULE_CLASS_NAME = 'Money'

INSTALLED_APPS_NAME = 'money.apps.MoneyConfig'

PLUGIN_CFG_UPDATE = {
    'money': {
        'nav_url': 'money_home',
        'nav_name': 'Бухгалтерия'}}

INSTALLED_URL = {
    'money': {
        'path': 'money/',
        'include': 'money.urls'}}

REPO_DATA = {
        'title': 'Бухгалтерия',
        'id_in_repo': '',
        'description': '',
        'module_name': 'money',
        'version': '1',
        'related_class_name': 'Money'
}

def demodata():
    context = 'Данных для установки нет'
    return context
