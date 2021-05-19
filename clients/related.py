from .forms import RelatedAddForm
from .models import Clients
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q


class AppRelated(object):
    prefix = 'clients'

    # если переменная имеет возможность иметь несколько uuid на одну запись, тогда здесь идет обрабтока такой возможности
    def checkUpdate(self, **kwargs):
        if kwargs['request_post']['clients-phone']:
            try:
                Clients.objects.get(phone=kwargs['request_post']['clients-phone'])
                return True
            except ObjectDoesNotExist:
                return False
        return False

    def checkRelatedAddForm(self, **kwargs):
        context= {}
        request_post = kwargs['request_post']
        if self.checkUpdate(request_post=request_post):
            get_client = Clients.objects.get(phone=request_post['clients-phone'])
            related_form = RelatedAddForm(request_post, prefix=self.prefix, instance=get_client)
            context['uuid'] = get_client.related_uuid
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
            get_client = Clients.objects.get(phone=request_post['clients-phone'])
            related_form = RelatedAddForm(request_post, prefix=self.prefix, instance=get_client)
            context['uuid'] = ''
            context['pk'] = get_client.pk
        else:
            related_form = RelatedAddForm(request_post, prefix=self.prefix)
            related_form.prefix = self.prefix
            context['uuid'] = ''
            context['pk'] = ''
        context['form'] = related_form
        return context

    def deleteRelatedMultipleUuid(self, **kwargs):
        dictt = kwargs['dictt']
        for k, v in dictt['deleteuuid'].items():
            get_client = Clients.objects.get(Q(related_uuid__icontains=k))
            changeUuid = get_client.related_uuid
            changeUuid.pop(k)
            get_client.related_uuid = changeUuid
            get_client.save()