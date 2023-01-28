from django import template
from django.utils.html import mark_safe
from django.http import HttpRequest

register = template.Library()

@register.simple_tag
def url_replace(req, **kwargs):
    query = req.GET.copy()
    for kwarg in kwargs:
        try:
            query.pop(kwarg)
        except KeyError:
            pass
    query.update(kwargs)
    return mark_safe(query.urlencode())


@register.simple_tag
def url_replace3(req: HttpRequest, **kwargs):
    query_strings = req.GET.dict()
    string = '?'
    for i in query_strings:
        string += f'{i}={query_strings[i]}&'
    return string[0:string.__len__()-1]

@register.simple_tag(takes_context=True)
def url_replace2(context, **kwargs):
    query = context['request'].GET.copy()
    for kwarg in kwargs:
        try:
            query.pop(kwarg)
        except KeyError:
            pass
    query.update(kwargs)
    return mark_safe(query.urlencode())



