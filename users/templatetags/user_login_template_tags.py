from django import template
from django.contrib.auth.models import User

register = template.Library()

@register.inclusion_tag('include/_login_error_tags.html')
def show_error_login():
    ddict = {}
    superuser = User.objects.filter(is_superuser=True).first()
    if superuser is None:
        ddict['error'] = 'superuser_is_none'
    return ddict
