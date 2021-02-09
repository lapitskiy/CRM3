from django import template
from django.db.models import Count
from plugins.models import Plugins
from django.conf import settings
import json
import requests
import io
import zipfile


register = template.Library()

@register.inclusion_tag('plugins/install_tags.html')
def install_plugin(arg1=0):
    context = {}
    try:
        context['json_check'] = True
        json_string = requests.get(settings.REPO_URL)
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
                            return context
                    except:
                        context['load_check'] = False
                        return context

        context['json_check'] = False
        return context
    except ValueError:
        context['json_check'] = False
        return context

def in_dictionary(key, dict):
    return key in dict