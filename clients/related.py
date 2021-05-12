from .forms import RelatedAddForm
from .models import Clients


class checkRelated(object):
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
        if self.checkUpdate(request_post=kwargs['request_post']):
            get_client = Clients.objects.get(phone=kwargs['request_post']['clients-phone'])
            related_form = RelatedAddForm(self.request.POST, prefix=self.prefix, instance=get_client)
        else:
            related_form = RelatedAddForm(kwargs['request_post'], prefix=self.prefix)
            related_form.prefix = self.prefix
        print('request_post ', kwargs['request_post'])
        print('related_form ', related_form)
        return related_form

