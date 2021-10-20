from django import template

register = template.Library()

@register.inclusion_tag('users/sidebar_users_menu_tags.html')
def show_menu():
    pass
    return