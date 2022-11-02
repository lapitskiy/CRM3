from django import template
from ..models import Storehouses
from ..utils import getStoresListByUser

register = template.Library()

@register.inclusion_tag('storehouse/related/tags/sidebar_storehouse_related_submenu_tags.html', takes_context=True)
def show_menu(context):
    #print('============================')
    #print('THIS request', context['request'])
    request = context['request']
    queryset = getStoresListByUser(user=request.user)
    context['storehouses'] = queryset
    return context

