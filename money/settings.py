from plugins.models import DesignPosition, DesignRelatedPlugin, Plugins

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
    # DesignPosition
    plugin = Plugins.objects.get(module_name=MODULE_NAME)
    check_plugin = DesignRelatedPlugin.objects.filter(related_plugin=plugin)
    if not check_plugin:
        design_obj = DesignPosition.objects.all()
        for obj in design_obj:
            DesignRelatedPlugin.objects.create(position=obj, related_plugin=plugin)

    context = 'Данные установлены'
    return context
