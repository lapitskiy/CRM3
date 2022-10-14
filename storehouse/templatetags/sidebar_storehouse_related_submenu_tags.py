from django import template
from ..models import Storehouses

register = template.Library()

@register.inclusion_tag('storehouse/related/tags/sidebar_storehouse_related_submenu_tags.html', takes_context=True)
def show_menu(context):
    query = Storehouses.objects.all()
    context['storehouses'] = query
    return context

