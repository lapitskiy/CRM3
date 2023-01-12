from .forms import RelatedAddForm
from .models import Money, Prepayment, RelatedUuid
from django.db.models import Q

class AppRelated(object):
    prefix = 'money'
    related_format = 'form'
    related_data_format = 'form'

    def checkUpdate(self, **kwargs):
        return False

    # если это связанный объект, который не имеет формы или не требует обновления, то возврщает True и пропускается в
    # utils checkRelatedIsValidDict, как не требующий добавления для проверки форимы и обновления текущей
    def passAddUpdate(self, **kwargs):
        return False

    # если это связанный объект, который не имеет формы или не требует обновления, то возврщает True и пропускается в
    # utils checkRelatedIsValidDict, как не требующий добавления для проверки форимы и обновления текущей
    def passEditUpdate(self, **kwargs):
        return False

    # если это не создание новой модели, а изминение старой на другую уже существующую, тогда мы должены произвести смену
    # uuid мужду этими моделями
    # return False or dict uudi convert
    def checkConvert(self, **kwargs):
        return False

    def submenuImportRelated(self, **kwargs):
        pass

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
        context['form'] = related_form
        if related_form.is_valid():
            context['valid'] = True
        else:
            context['valid'] = False
        return context

    def checkRelatedEditForm(self, **kwargs):
        context= {}
        request_post = kwargs['request_post']
        if self.checkUpdate(request_post=request_post):
            context['uuid'] = ''
            context['pk'] = ''
        else:
            get_money = Money.objects.get(uuid__related_uuid=kwargs['uuid'][0])
            related_form = RelatedAddForm(request_post, prefix=self.prefix, instance=get_money)
            related_form.prefix = self.prefix
            context['pk'] = get_money.pk
            context['uuid'] = ''
        context['form'] = related_form
        if related_form.is_valid():
            context['valid'] = True
        else:
            context['valid'] = False
        return context

    def deleteRelatedMultipleUuid(self, **kwargs):
        pass

    def checkCleanQueryset(self, **kwargs):
        pass

    def passCleanQueryset(self, **kwargs):
        return True

    def saveForm(self, **kwargs):
        if kwargs['method'] == 'add':
            related_dict = kwargs['related_form_dict']
            form_from_dict = related_dict['form']
            form_add = form_from_dict.save(commit=False)
            print('related_dict 1', related_dict['uuid'])
            make_uuid_obj = RelatedUuid(related_uuid=related_dict['uuid'])
            make_uuid_obj.save()
            form_add.save()
            form_add.uuid.add(make_uuid_obj)
            form_add.save()
            print('money saveform: ', form_from_dict.cleaned_data.get('is_pay'))
            print('money pk: ', form_add.pk)

            if form_from_dict.cleaned_data.get('is_pay'):
                prepay = Prepayment(money=form_add, prepayment=form_add.money)
                prepay.save()
        if kwargs['method'] == 'edit':
            related_dict = kwargs['related_form_dict']
            form_from_dict = related_dict['form']
            form_add = form_from_dict.save(commit=False)
            form_add.save()

    def linkGetReleatedData(self, **kwargs):
        uudi_filter_related_list = []
        return uudi_filter_related_list
