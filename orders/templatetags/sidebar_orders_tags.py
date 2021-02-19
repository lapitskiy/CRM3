from django import template
from orders.models import Status

register = template.Library()

@register.inclusion_tag('orders/sidebar_orders_tags.html')
def show_orders_status(arg1='he11o', arg2='wor1d'):
    status = Status.objects.all()
    #categories = Category.objects.annotate(cnt=Count('get_category')).filter(cnt__gt=0)
    return {'status' : status, 'arg1' : arg1, 'arg2' : arg2}
