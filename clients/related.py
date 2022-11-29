from .forms import RelatedAddForm
from .models import Clients
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q


class AppRelated(object):
    prefix = 'clients'
    related_format = 'form'

    # если переменная имеет возможность иметь несколько uuid на одну запись, тогда здесь идет обработка такой возможности
    # например на один номер телефона может быть два заказа, и тут идет  проветка нет ли такого телефона в базе уже
    def checkUpdate(self, **kwargs):
        if kwargs['request_post']['clients-phone']:
            try:
                Clients.objects.get(phone=kwargs['request_post']['clients-phone'])
                return True
            except ObjectDoesNotExist:
                return False
        return False

    # если это связанный объект, который не имеет формы или не требует обновления, то возврщает True и пропускается в
    # utils checkRelatedIsValidDict, как не требующий добавления для проверки форимы и обновления текущей
    def passAddUpdate(self, **kwargs):
        return False

    # если это связанный объект, который не имеет формы или не требует обновления, то возврщает True и пропускается в
    # utils checkRelatedIsValidDict, как не требующий добавления для проверки формы и обновления текущей
    def passEditUpdate(self, **kwargs):
        return False

    # если это не создание новой модели, а изминение старой на другую уже существующую, тогда мы должены произвести смену
    # uuid мужду этими моделями
    # по сути это select форма, и если мы редактируем заказ, чтобы была возможность проверить, есть ли уже такой select
    # и если есть, просто связать заказ и уже существую модель
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
        context['request_post'] = kwargs['request_post']
        if self.checkUpdate(request_post=request_post):
            get_client = Clients.objects.get(phone=request_post['clients-phone'])
            related_form = RelatedAddForm(request_post, prefix=self.prefix, instance=get_client)
            #print('related_form: ', related_form)
            context['uuid'] = get_client.related_uuid
            context['pk'] = get_client.pk
            if related_form.is_valid():
                context['valid'] = True
            else:
                context['valid'] = False
        else:
            related_form = RelatedAddForm(request_post, prefix=self.prefix)
            related_form.prefix = self.prefix
            if related_form.is_valid():
                context['valid'] = True
            else:
                context['valid'] = False
            if request_post['clients-phone'] == '':
                print('phone ', request_post['clients-phone'])
                context['valid'] = True
            context['uuid'] = ''
            context['pk'] = ''
        context['form'] = related_form
        print('clinet request_post ', context['request_post'])
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
            #print('kwargs data', kwargs['data'])
            qry = Clients.objects.filter(Q(phone__icontains=kwargs['data'])).values()
            return [entry for entry in qry]

    def checkCleanQueryset(self, **kwargs):
        pass

    def passCleanQueryset(self, **kwargs):
        return True

    def saveForm(self, **kwargs):
        related_dict = kwargs['related_dict']
        form_from_dict = related_dict['form']
        request = kwargs['request']
        #print('valid ', form_from_dict.is_valid())
        ##print('tyt 1 ', form_from_dict)
        #print('tyt 2 ', form_from_dict.cleaned_data.get('id_clients-phone'))
        #print('tyt 22 ', form_from_dict.cleaned_data.get('clients-phone'))
        #print('tyt 23 ', form_from_dict.cleaned_data['phone'])
        if request.POST['clients-phone'] == '':
            print('tyt 3')
            pass
        else:
            print('tyt 4')
            form_add = form_from_dict.save(commit=False)
            form_add.related_uuid = related_dict['uuid']
            form_add.save()
            print('save contact')