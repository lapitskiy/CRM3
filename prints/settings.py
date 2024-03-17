from plugins.models import DesignPosition, DesignRelatedPlugin, Plugins

# файл удаляется после установки
MODULE_NAME = 'prints'
MODULE_CLASS_NAME = 'Prints'

INSTALLED_APPS_NAME = 'prints.apps.PrintConfig'

PLUGIN_CFG_UPDATE = {
    'prints': {
        'nav_url': 'prints_home',
        'nav_name': 'Печать'}}

INSTALLED_URL = {
    'prints': {
        'path': 'prints/',
        'include': 'prints.urls'}}

REPO_DATA = {
        'title': 'Печать',
        'id_in_repo': '',
        'description': '',
        'module_name': 'prints',
        'version': '1',
        'related_class_name': 'Prints'
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