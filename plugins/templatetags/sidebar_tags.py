from django import template
from django.db.models import Count
from plugins.models import PluginsCategory

register = template.Library()

#@register.simple_tag(name='get_list_categories')
#def get_categories():
#    return Category.objects.all()

@register.inclusion_tag('plugins/list_categories.html')
def show_categories(arg1='he11o', arg2='wor1d'):
    categories = PluginsCategory.objects.all()
    #categories = Category.objects.annotate(cnt=Count('get_category')).filter(cnt__gt=0)
    print(categories)
    return {'categories' : categories, 'arg1' : arg1, 'arg2' : arg2}
