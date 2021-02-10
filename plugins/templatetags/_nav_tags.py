from django import template
from plugins import settings_plugin

register = template.Library()

@register.inclusion_tag('../templates/include/_nav.html')
def navigation():
    context = {'nav' : settings_plugin.PLUGIN_CFG}
    return context
