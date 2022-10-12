from django import template
from orders.models import Orders, Status, Category_service

register = template.Library()

@register.inclusion_tag('related/tags/sidebar_orders_related_submenu_tags.html')
def show_menu():
    pass

