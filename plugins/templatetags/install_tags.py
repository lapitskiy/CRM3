from django import template
from django.db.models import Count
from plugins.models import Plugins
from plugins import settings_plugin

from collections import OrderedDict
from django.apps import apps
from django.core import management

import json
import requests
import io
import zipfile

import ast

import importlib

import re

register = template.Library()

@register.inclusion_tag('plugins/install_tags.html')
def install_plugin(arg1=0):
    context = {}
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
                        return context

                    except:
                        context['load_check'] = False
                        return context

        context['json_check'] = False
        return context
    except ValueError:
        context['json_check'] = False
        return context



def impliment(moduleName):
    modulePath = moduleName +'.install'
    print('modulePath', modulePath)
    app_module = importlib.import_module(modulePath)
    print('app_module', app_module)
    print('app_module.apps_install_name ', app_module.INSTALLED_APPS_NAME)

    with open('plugins/settings_plugin.py', 'r', encoding="utf-8") as file:
        content = file.read()
        print('content ',content)
    #tag = re.findall(r'INSTALLED_APPS_ADD+.*\W+', content)

    # ADD APPS
    tag = re.findall(r'INSTALLED_APPS_ADD = (\[.*\])', content)
    listt = ast.literal_eval(tag[0])
    listt.append(app_module.INSTALLED_APPS_NAME)
    content = re.sub(r'(INSTALLED_APPS_ADD = )\[.*\]', r'\1' + str(listt), content)

    # ADD CFG
    tag = re.findall(r'PLUGIN_CFG = (\{.*\})', content)
    dictt = ast.literal_eval(tag[0])
    dictt.update(app_module.PLUGIN_CFG_UPDATE)
    print('dictt ', dictt)
    content = re.sub(r'(PLUGIN_CFG = )\{.*\}', r'\1' + str(dictt), content)
    print('content ', content)

    # ADD URL
    tag = re.findall(r'PLUGIN_URLS = (\[.*\])', content)
    print('tag ', tag)
    listt = ast.literal_eval(tag[0])
    print('listt ', listt)
    listt.append(app_module.INSTALLED_URL)
    print('listt ', listt)
    content = re.sub(r'(PLUGIN_URLS = )\[.*\]', r'\1' + str(listt), content)
    print('content ', content)

    apps.app_configs = OrderedDict()
    apps.apps_ready = apps.models_ready = apps.loading = apps.ready = False
    apps.clear_cache()

    with open('plugins/settings_plugin.py', 'w', encoding="utf-8") as file:
        file.write(content)

    apps.populate(settings.INSTALLED_APPS)
    management.call_command('makemigrations', app_module.INSTALLED_APPS_NAME, interactive=False)
    management.call_command('migrate', app_module.INSTALLED_APPS_NAME, interactive=False)



def in_dictionary(key, dict):
    return key in dict