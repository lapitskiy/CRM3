from django import template
from django.db.models import Count
from plugins.models import Plugins
import json
import requests


register = template.Library()

@register.inclusion_tag('plugins/repository_tags.html')
def load_repository():
    try:
        json_string = requests.get('http://127.0.0.1:8001/plugins/api/?format=json')
        data = json.loads(json_string.text)
        print('json_string ', data)

    except ValueError:
        return {'error' : 'json_string'}
    return {'load_plugins' : data}