from django import template
from django.conf import settings


register = template.Library()

@register.inclusion_tag('include/_nav.html')
def navigation(arg1=0):
    context = {}
    for item in settings.INSTALLED_APPS:
        if 'django.' not in item:
            context[item] = ''


    return
