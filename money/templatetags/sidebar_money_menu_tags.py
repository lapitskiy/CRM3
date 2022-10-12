from django import template
from plugins.utils import RelatedMixin

register = template.Library()

@register.inclusion_tag('money/sidebar_money_menu_tags.html')
def show_menu():
    Relateddata = RelatedMixin()
    Relateddata.related_module_name = 'money'
    related_submenu = Relateddata.relatedImportSubmenu()
    print('related_submenu ', related_submenu)
    context = {'relatedmenu': related_submenu}
    print('submenu', context)
    return context

