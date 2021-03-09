from django import template

register = template.Library()

@register.inclusion_tag('clients/sidebar_clients_menu_tags.html')
def show_menu():
    pass
    return
