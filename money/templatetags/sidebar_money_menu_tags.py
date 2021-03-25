from django import template

register = template.Library()

@register.inclusion_tag('money/sidebar_money_menu_tags.html')
def show_menu():
    pass
    return
