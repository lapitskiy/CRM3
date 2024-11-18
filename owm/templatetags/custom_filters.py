from django import template

register = template.Library()

@register.filter
def get_row_class(sale_qty):
    if sale_qty < 1:
        return "alert-danger"
    elif sale_qty < 10:
        return "alert-warning"
    else:
        return "alert-success"