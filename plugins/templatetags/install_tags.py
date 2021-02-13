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

from ..models import Plugins, PluginsCategory

register = template.Library()

@register.inclusion_tag('plugins/install_tags.html')
def install_plugin(arg1=0):
    context = {}
    context['json_check'] = False
    context['load_check'] = False
    context['makemigrations_check'] = False
    try:
        context['json_check'] = True
        json_string = requests.get(settings_plugin.REPO_URL)
        data = json.loads(json_string.text)
        for item in data:
            if in_dictionary('id', item):
                if item['id']==arg1:
                    context['install_data'] = item
                    # repack arch zip
                    r = requests.get(item['zipfile'])
                    try:
                        with r, zipfile.ZipFile(io.BytesIO(r.content)) as archive:
                            archive.extractall()
                        context['load_check'] = True

                        impliment(item['module_name'])

                        add_plugin_in_db(data)

                    except:
                        return context
                    try:
                        makemigrations(item['module_name'])

                        context['makemigrations_check'] = True
                        return context
                    except:
                        return context



        return context
    except ValueError:
        return context



def impliment(moduleName):
    modulePath = moduleName +'.install'
    app_module = importlib.import_module(modulePath)

    with open('plugins/settings_plugin.py', 'r', encoding="utf-8") as file:
        content = file.read()

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

def makemigrations(module):
    try:
        management.call_command('makemigrations', module, interactive=False)
        print('MAKE OK')
        #management.call_command('migrate --check', module, interactive=False)
        #print('MIGRATE OK', test)
        return True
    except:
        # raise Exception("Unable to perform migration)
        return True


def add_plugin_in_db(data):
    plugin = Plugins
    plugin.id_in_repo = data['id']
    plugin.title = data['title']
    plugin.module_name = data['module_name']
    plugin.description =  data['description']
    plugin.photo = data['photo']
    plugin.zipfile = data['zipfile']
    plugin.is_active = data['is_active']
    plugin.category = data['category']
    plugin.version = data['version']
    plugin.save()
    #тут добавить добалвения плагина в базу плагинов и потом там уже мигрировать




def in_dictionary(key, dict):
    return key in dict