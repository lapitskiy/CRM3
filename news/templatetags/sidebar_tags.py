from django import template
from django.db.models import Count
from news.models import Category

register = template.Library()

@register.simple_tag(name='get_list_categories')
def get_categories():
    return Category.objects.all()

@register.inclusion_tag('news/list_categories.html')
def show_categories(arg1='he11o', arg2='wor1d'):
    #categories = Category.objects.all()
    categories = Category.objects.annotate(cnt=Count('get_news')).filter(cnt__gt=0)
    print(categories)
    return {'categories' : categories, 'arg1' : arg1, 'arg2' : arg2}
