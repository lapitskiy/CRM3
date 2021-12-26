from .forms import RelatedAddForm
from .models import Clients
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q


class AppRelated(object):
    prefix = 'clients'
    related_format = 'data'

    # если переменная имеет возможность иметь несколько uuid на одну запись, тогда здесь идет обрабтока такой возможности
    def checkUpdate(self, **kwargs):
        if kwargs['request_post']['clients-phone']:
            try:
                Clients.objects.get(phone=kwargs['request_post']['clients-phone'])
                print('checkUpdate TRUE')
                return True
            except ObjectDoesNotExist:
                print('checkUpdate False')
                return False
        return False

    # если это связанный объект, который не имеет формы или не требует обновления, то возврщает True и пропускается в
    # utils checkRelatedIsValidDict, как не требующий добавления для проверки форимы и обновления текущей
    def passEditUpdate(self, **kwargs):
        return False

    # если это не создание новой модели, а изминение старой на другую уже существующую, тогда мы должены произвести смену
    # uuid мужду этими моделями
    # return False or dict uudi convert
    def checkConvert(self, **kwargs):
        if kwargs['uuid']:
            try:
                get_client_before = Clients.objects.get(Q(related_uuid__icontains=kwargs['uuid'][0]))
                get_client_now = Clients.objects.get(phone=kwargs['request_post']['clients-phone'])
                if get_client_before.pk != get_client_now.pk:
                    new_uuid_dict = get_client_now.related_uuid
                    new_uuid_dict.update({kwargs['uuid'][0]:''})
                    return new_uuid_dict
            except ObjectDoesNotExist:
                return False
        return False

    def checkRelatedAddForm(self, **kwargs):
        context= {}
        request_post = kwargs['request_post']
        #print('request clients-phone checkRelatedAddForm: ', request_post['clients-phone'])
        #print('checkUpdate ', self.checkUpdate(request_post=request_post))
        if self.checkUpdate(request_post=request_post):
            get_client = Clients.objects.get(phone=request_post['clients-phone'])
            #print('get clinet: ', get_client)
            print('CLIENTS IF request_post ', request_post)
            related_form = RelatedAddForm(request_post, prefix=self.prefix, instance=get_client)
            #print('related_form: ', related_form)
            context['uuid'] = get_client.related_uuid
            context['pk'] = get_client.pk
        else:
            print('CLIENTS ELSE request_post ', request_post)
            related_form = RelatedAddForm(request_post, prefix=self.prefix)
            related_form.prefix = self.prefix
            if related_form.is_valid():
                print('phone valid')
            else:
                print('phone not valid')
            context['uuid'] = ''
            context['pk'] = ''
        print('Related - Client')
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

    def getAjaxRelatedList(self, **kwargs):
        if kwargs['data']:
            print('kwargs data', kwargs['data'])
            qry = Clients.objects.filter(Q(phone__icontains=kwargs['data'])).values()
            return [entry for entry in qry]