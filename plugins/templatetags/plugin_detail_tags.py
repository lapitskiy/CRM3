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

from plugins.models import Plugins, DesignRelatedPlugin, RelatedFormat

register = template.Library()

@register.inclusion_tag('include/_plugins_detail_tags.html')
def action_plugin(arg1=0, tag='', form_related=None, form_relatedformat=None, form_designposition=None):
    context = {}
    plugin = Plugins.objects.get(pk=arg1)
    context['id'] = arg1
    context['tag'] = tag
    context['form_related'] = form_related
    context['form_relatedformat'] = form_relatedformat
    context['form_designposition'] = form_designposition
    context['active_check'] = plugin.is_active
    context['isRelated'] = plugin.related.all()
    context['isRelatedFormat'] = RelatedFormat.objects.all()
    context['isDesignRelatedPlugin'] = DesignRelatedPlugin.objects.filter(related_plugin=arg1)
    context['delete_check'] = False
    context['copydata'] = False
    if tag == 'active' and not context['active_check']:
        print('ACTIVE')
        print('plugin', plugin)
        print('arg1', arg1)
        plugin.is_active = True
        plugin.save()
        context['active_check'] = True
        context['plugin_url'] = plugin.get_absolute_url()
        return context

    if tag == 'deactive' and context['active_check']:
        print('DEACTIVE')
        plugin.is_active = False
        plugin.save()
        context['active_check'] = False
        context['plugin_url'] = plugin.get_absolute_url()
        return context

    if tag == 'delete' and not context['active_check']:
        context['delete_check'] = True
        print('DELETE')
        # доделать удаление
        with open('plugins/settings_plugin.py', 'r', encoding="utf-8") as file:
            content = file.read()

        plugin_name = plugin.module_name

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
        modulePath = plugin.module_name + '.settings'
        app_module = importlib.import_module(modulePath)
        context['info'] = app_module.demodata()
        context['plugin_url'] = plugin.get_absolute_url()
        context['copydata'] = True
        return context

    if tag == 'related':
        print('RELATED')
        return context
    print('tag', tag)
    return context

