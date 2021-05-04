from django import template
from plugins.utils import RelatedMixin
from plugins.models import Plugins

register = template.Library()

@register.inclusion_tag('money/sidebar_money_menu_tags.html')
def show_menu():
    RelatedMoney = RelatedMixin()
    RelatedMoney.related_module_name = 'money'
    related_plugin_list = RelatedMoney.checkRelated()
    data_related_list = []
    if related_plugin_list:
        for x in related_plugin_list:
            data_related_dict = {}
            data_related_dict['name'] = x.title
            data_related_dict['module_name'] = x.module_name
            data_related_list.append(data_related_dict)
    context = {'relatedmenu': data_related_list}
    return context

