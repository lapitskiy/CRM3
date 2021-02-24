from django import template
from plugins import settings_plugin
from django.conf import settings
import re
from django.apps import apps
from collections import OrderedDict
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
import os
import shutil
import importlib

from plugins.models import Plugins

register = template.Library()

@register.inclusion_tag('plugins/plugins_tags.html')
def action_plugin(arg1=0, tag=''):
    context = {}
    context['id'] = arg1
    context['tag'] = tag
    context['active_check'] = Plugins.objects.get(id=arg1).is_active
    context['delete_check'] = False
    print('is_active', context['active_check'])

    if tag == 'active' and not context['active_check']:
        print('ACTIVE')
        Plugins.objects.update(is_active=True)
        context['active_check'] = True
        context['plugin_url'] = Plugins.objects.get(id=arg1).get_absolute_url()
        return context

    if tag == 'deactive' and context['active_check']:
        print('DEACTIVE')
        Plugins.objects.update(is_active=False)
        context['active_check'] = False
        context['plugin_url'] = Plugins.objects.get(id=arg1).get_absolute_url()
        return context

    if tag == 'delete' and not context['active_check']:
        context['delete_check'] = True
        print('DELETE')
        # доделать удаление
        with open('plugins/settings_plugin.py', 'r', encoding="utf-8") as file:
            content = file.read()

        plugin_name = Plugins.objects.get(id=arg1).module_name

        # DEL APPS
        installes_apps = [i for i in settings_plugin.INSTALLED_APPS_ADD if plugin_name not in i]
        print('installes_apps: ', installes_apps)
        content = re.sub(r'(INSTALLED_APPS_ADD = )\[.*\]', r'\1' + str(installes_apps), content)


        # DEL CFG
        pop_order = settings_plugin.PLUGIN_CFG
        if plugin_name in pop_order:
            del pop_order[plugin_name]
        content = re.sub(r'(PLUGIN_CFG = )\{.*\}', r'\1' + str(pop_order), content)

        # DEL URL
        pop_order = settings_plugin.PLUGIN_URLS
        if plugin_name in pop_order:
            del pop_order[plugin_name]
        content = re.sub(r'(PLUGIN_URLS = )\{.*\}', r'\1' + str(pop_order), content)

        # DEL MYSQL DATA
        delete_plugin = get_object_or_404(Plugins, pk=arg1).delete()

        # reset apps

        path = apps.get_app_config(plugin_name).path

        apps.app_configs = OrderedDict()
        apps.apps_ready = apps.models_ready = apps.loading = apps.ready = False
        apps.clear_cache()
        apps.populate(settings.INSTALLED_APPS)
        with open('plugins/settings_plugin.py', 'w', encoding="utf-8") as file:
            file.write(content)
        #path = os.path.join('', plugin_name)
        #path = os.path.abspath(os.path.dirname(__file__))
        print('PATH ', path)
        shutil.rmtree(path)
        print('PLUGIN DELETE')
        return context

    if tag == 'demodata':
        print('DEMODATA')
        modulePath = Plugins.objects.get(id=arg1).module_name + '.install'
        app_module = importlib.import_module(modulePath)
        app_module.demodata()
        context['plugin_url'] = Plugins.objects.get(id=arg1).get_absolute_url()
        return context

    return context

