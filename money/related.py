from .forms import RelatedAddForm
from .models import Money
from django.db.models import Q

class AppRelated(object):
    prefix = 'money'

    def checkUpdate(self, **kwargs):
        return False

    # если это не создание новой модели, а изминение старой на другую уже существующую, тогда мы должены произвести смену
    # uuid мужду этими моделями
    # return False or dict uudi convert
    def checkConvert(self, **kwargs):
        return False

    def checkRelatedAddForm(self, **kwargs):
        context = {}
        request_post = kwargs['request_post']
        if self.checkUpdate(request_post=request_post):
            context['uuid'] = ''
            context['pk'] = ''
        else:
            related_form = RelatedAddForm(request_post, prefix=self.prefix)
            related_form.prefix = self.prefix
            context['uuid'] = ''
            context['pk'] = '1'
        print('Related - Money')
        if related_form.is_valid():
            print('money valid')
        else:
            print('money not valid')
        print('pk ', context['pk'])
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

    def deleteRelatedMultipleUuid(self, **kwargs):
        pass
