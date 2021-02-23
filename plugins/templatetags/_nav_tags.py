from django import template
from plugins import settings_plugin
from plugins.models import Plugins


register = template.Library()

@register.inclusion_tag('../templates/include/_nav.html')
def navigation():
    active_plugin = Plugins.objects.filter(is_active=True)
    print('active_plugin: ', active_plugin)
    tag = {}
    for key in settings_plugin.PLUGIN_CFG.keys():
        for active in active_plugin:
            if key == active.module_name:
                tag.update(key=settings_plugin.PLUGIN_CFG[key])
    context = {'nav': tag}
    return context
