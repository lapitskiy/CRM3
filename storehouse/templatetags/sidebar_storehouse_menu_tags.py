from django import template

register = template.Library()

@register.inclusion_tag('storehouse/sidebar_storehouse_menu_tags.html')
def show_menu():
    pass
    return

@register.inclusion_tag('storehouse/settings/sidebar_storehouse_menu_settings_tags.html')
def show_storehouse_menu():
    pass
    return