from django import template

register = template.Library()

@register.inclusion_tag('owm/sidebar_menu.html')
def show_menu():
    pass
