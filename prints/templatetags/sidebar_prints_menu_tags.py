from django import template

register = template.Library()

@register.inclusion_tag('prints/sidebar_prints_menu_tags.html')
def show_menu():
    pass
    return
