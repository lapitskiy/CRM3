from .forms import RelatedAddForm
from .models import Money
from django.db.models import Q

class AppRelated(object):
    prefix = 'money'

    def checkUpdate(self, **kwargs):
        return False

    def checkRelatedAddForm(self, **kwargs):
        context = {}
        request_post = kwargs['request_post']
        if self.checkUpdate(request_post=request_post):
            pass
        else:
            related_form = RelatedAddForm(request_post, prefix=self.prefix)
            related_form.prefix = self.prefix
            context['uuid'] = ''
        print('request_post ', request_post)
        print('related_form ', related_form)
        context['form'] = related_form
        return context

    def checkRelatedEditForm(self, **kwargs):
        context= {}
        request_post = kwargs['request_post']
        if self.checkUpdate(request_post=request_post):
            context['uuid'] = ''
            context['pk'] = ''
        else:
            get_money = Money.objects.get(Q(related_uuid__icontains=kwargs['uuid'][0]))
            related_form = RelatedAddForm(request_post, prefix=self.prefix, instance=get_money)
            related_form.prefix = self.prefix
            context['pk'] = get_money.pk
            context['uuid'] = ''
        context['form'] = related_form
        return context
