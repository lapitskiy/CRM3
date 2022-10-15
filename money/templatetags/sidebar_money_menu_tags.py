from django import template
from plugins.utils import RelatedMixin

register = template.Library()

@register.inclusion_tag('money/sidebar_money_menu_tags.html', takes_context=True)
def show_menu(context):
    #print('============================')
    #request2 = context['request']
    #print('user ', request.user)
    #print('user2 ', request2.user)
    #print('MOney tags! context', context['request'])
    Relateddata = RelatedMixin()
    Relateddata.related_module_name = 'money'
    related_submenu = Relateddata.relatedImportSubmenu()
    #print('related_submenu ', related_submenu)
    context['relatedmenu'] = related_submenu
    #print('submenu', context)
    return context

