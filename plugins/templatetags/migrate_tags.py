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

@register.inclusion_tag('plugins/migrate_tags.html')
def migrate_plugin(arg1=0):
    context = {}
    context['id'] = arg1
    context['migrate_check'] = False
    plugin = Plugin.objects.get(id_in_repo=arg1)
    print('TRY migrate')
    management.call_command('migrate', plugin.module_name, interactive=False)
    print('migrate OK')
    plugin.is_migrate = True
    plugin.is_active = True
    plugin.save()
    context['migrate_check'] = True
    return context
