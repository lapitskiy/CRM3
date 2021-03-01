from django import template
from plugins import settings_plugin
from plugins.models import Plugins


register = template.Library()

@register.inclusion_tag('../templates/include/_nav.html')
def navigation():
    active_plugin = Plugins.objects.filter(is_active=True)
    tag = {}
    for key in settings_plugin.PLUGIN_CFG.keys():
        for active in active_plugin:
            if key == active.module_name:
                dictt = {key: settings_plugin.PLUGIN_CFG[key]}
                tag.update(dictt)
    context = {'nav': tag}
    return context

