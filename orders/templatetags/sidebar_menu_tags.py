from django import template
from orders.models import Orders, Status, Category_service

register = template.Library()

@register.inclusion_tag('orders/sidebar_menu_tags.html')
def show_menu():
    status = Status.objects.all()
    category_service = Category_service.objects.all()
    #print('status ', status)
    _dict = {}
    return_dict = {}
    for pk in status:
        _dict_for = {}
        _dict_for['title'] = pk.title
        _dict_for['count'] = Orders.objects.filter(status=pk.pk).count()
        _dict[pk.pk] = _dict_for
    return_dict['status'] = _dict
    _dict = {}
    for pk in category_service:
        _dict_for = {}
        _dict_for['name'] = pk.name
        _dict[pk.pk] = _dict_for
    return_dict['category_service'] = _dict
    #print('_dict', _dict)
    return return_dict

@register.inclusion_tag('settings/sidebar_menu_settings_tags.html')
def show_settings_menu():
    pass
    #categories = Category.objects.annotate(cnt=Count('get_category')).filter(cnt__gt=0)
    return
