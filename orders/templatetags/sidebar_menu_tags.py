from django import template
from orders.models import Orders, Status

register = template.Library()

@register.inclusion_tag('orders/sidebar_menu_tags.html')
def show_menu():
    status = Status.objects.all()
    print('status ', status)
    _dict = {}
    for pk in status:
        _dict_for = {}
        _dict_for['title'] = pk.title
        _dict_for['count'] = Orders.objects.filter(status=pk.pk).count()
        _dict[pk.pk] = _dict_for
    print('_dict', _dict)
    return {'status' : _dict}

@register.inclusion_tag('settings/sidebar_menu_settings_tags.html')
def show_settings_menu():
    pass
    #categories = Category.objects.annotate(cnt=Count('get_category')).filter(cnt__gt=0)
    return
