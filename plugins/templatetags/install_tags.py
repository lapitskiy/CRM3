from django import template
from plugins import settings_plugin
from collections import OrderedDict
from django.apps import apps
from django.conf import settings
from django.core import management
import json
import requests
import io
import zipfile
import ast
import importlib
import re

from plugins.models import Plugins, PluginsCategory

register = template.Library()

@register.inclusion_tag('plugins/install_tags.html')
def install_plugin(arg1=0, tag=''):
    context = {}
    context['id'] = arg1
    context['tag'] = tag
    if tag=='install':
        context = install(context)
    if 'migrate' in tag:
        context['moduleName'] = tag[tag.find('-')+1:]
        context = plugin_migrate(context)
    return context



def install(context):
    context['json_check'] = False
    context['load_check'] = False
    context['makemigrations_check'] = False
    print('TYT1')
    try:
        if Plugins.objects.get(id_in_rep=context['id']) != None:
            context['have_check'] = True
            context['plugin_url'] = Plugins.objects.get(id_in_rep=context['id']).get_absolute_url()
            return context
    except Plugins.DoesNotExist:
        pass
    print('TYT2')
    json_string = requests.get(settings_plugin.REPO_URL)
    data = json.loads(json_string.text)
    context['json_check'] = True
    data_id = {}
    for item in data:
        if in_dictionary('id', item):
            if item['id'] == context['id']:
                data_id = item
                context['install_data'] = item
                context['migrateUrl'] = 'migrate-'+item['module_name']
                # repack arch zip
                print('TYT3')
                r = requests.get(item['zipfile'])
                with r, zipfile.ZipFile(io.BytesIO(r.content)) as archive:
                    archive.extractall()
                context['load_check'] = True
                print('TYT4')
                impliment(item['module_name'])
                print('install_tags.py: impliment OK')
                add_plugin_in_db(data_id)
                print('install_tags.py:  add_plugin_in_db OK')
                return context
    return context


def impliment(moduleName):
    modulePath = moduleName +'.install'
    app_module = importlib.import_module(modulePath)

    with open('plugins/settings_plugin.py', 'r', encoding="utf-8") as file:
        content = file.read()
    print('TYT5')
    # ADD APPS
    tag = re.findall(r'INSTALLED_APPS_ADD = (\[.*\])', content)
    listt = ast.literal_eval(tag[0])
    listt.append(app_module.INSTALLED_APPS_NAME)
    content = re.sub(r'(INSTALLED_APPS_ADD = )\[.*\]', r'\1' + str(listt), content)

    # ADD CFG
    tag = re.findall(r'PLUGIN_CFG = (\{.*\})', content)
    dictt = ast.literal_eval(tag[0])
    dictt.update(app_module.PLUGIN_CFG_UPDATE)
    content = re.sub(r'(PLUGIN_CFG = )\{.*\}', r'\1' + str(dictt), content)

    # ADD URL
    tag = re.findall(r'PLUGIN_URLS = (\{.*\})', content)
    dictt = ast.literal_eval(tag[0])
    dictt.update(app_module.INSTALLED_URL)
    content = re.sub(r'(PLUGIN_URLS = )\{.*\}', r'\1' + str(dictt), content)

    with open('plugins/settings_plugin.py', 'w', encoding="utf-8") as file:
        file.write(content)

    settings.INSTALLED_APPS += (app_module.INSTALLED_APPS_NAME,)
    apps.app_configs = OrderedDict()
    apps.apps_ready = apps.models_ready = apps.loading = apps.ready = False
    #apps.ready = False
    apps.clear_cache()
    apps.populate(settings.INSTALLED_APPS)
    print('APPS INSTALL ADD')
        #from django.utils import autoreload
        #print('MAKE RELODA')
        #autoreload.restart_with_reloader()


def plugin_migrate(context):
    try:
        management.call_command('makemigrations', context['moduleName'], interactive=False)
        management.call_command('migrate', context['moduleName'], interactive=False)
        context['make_check'] = True
        context['migrate_check'] = True
        print('MIGRATE OK')
        return context
    except:
        context['make_check'] = False
        context['migrate_check'] = False
        # raise Exception("Unable to perform migration)
        return context


def add_plugin_in_db(data):
    print('data ', data)
    plugin = Plugins()
    plugin.title = data['title']
    plugin.id_in_rep = data['id']
    plugin.module_name = data['module_name']
    plugin.description = data['description']
    plugin.photo = data['photo']
    plugin.zipfile = data['zipfile']
    plugin.category_id = data['category']
    plugin.version = data['version']
    plugin.save(force_insert=True)
    print('SAVE')
    #тут добавить добалвения плагина в базу плагинов и потом там уже мигрировать




def in_dictionary(key, dict):
    return key in dict