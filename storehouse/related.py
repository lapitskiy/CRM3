from .forms import RelatedAddForm
from .models import Storehouses, StoreRelated
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

class AppRelated(object):
    prefix = 'storehouse'
    related_format = 'select'

    # если переменная имеет возможность иметь несколько uuid на одну запись, тогда здесь идет обрабтока такой возможности и возвращается
    # true - пример сомтреть в модуле clients.related
    def checkUpdate(self, **kwargs):
        return False

    # если это связанный объект, который не имеет формы или не требует обновления, то возврщает True и пропускается в
    # utils checkRelatedIsValidDict, как не требующий добавления для проверки форимы и обновления текущей
    def passAddUpdate(self, **kwargs):
        return False

    # если это связанный объект, который не имеет формы или не требует обновления, то возврщает True и пропускается в
    # utils checkRelatedIsValidDict, как не требующий добавления для проверки форимы и обновления текущей
    # пример prints.related
    # вызывается в utils.checkRelatedIsValidDict
    def passEditUpdate(self, **kwargs):
        return True

    # если это не создание новой модели, а изминение старой на другую уже существующую, тогда мы должены произвести смену
    # uuid мужду этими моделями
    # по сути это select форма, и если мы редактируем заказ, чтобы была возможность проверить, есть ли уже такой select
    # и если есть, просто связать заказ и уже существую модель
    # return False or dict uudi convert
    # --> пример в clients.related
    def checkConvert(self, **kwargs):
        return False

    # проверка, надо ли добавлять форму после отправки данных в виде POST
    def checkRelatedAddForm(self, **kwargs):
        context= {}
        request_post = kwargs['request_post']

        if 'request' in kwargs:
            request = kwargs['request']
        #print('request clients-phone checkRelatedAddForm: ', request_post['clients-phone'])
        #print('checkUpdate ', self.checkUpdate(request_post=request_post))
        if self.checkUpdate(request_post=request_post):
            pass
        else:
            print('request', request)
            related_form = RelatedAddForm(request_post, prefix=self.prefix, request=request)
            related_form.prefix = self.prefix
            if related_form.is_valid():
                print('sotre valid')
            else:
                print('store not valid')
            context['uuid'] = ''
            context['pk'] = ''
        print('Related - Store')
        context['form'] = related_form
        return context

    def checkRelatedEditForm(self, **kwargs):
        pass

    def deleteRelatedMultipleUuid(self, **kwargs):
        pass

    def submenuImportRelated(self, **kwargs):
        pass

    def checkCleanQueryset(self, **kwargs):
        data_uuid_related_list = []
        self.request = kwargs['request']
        #result_queryset = []
        result_queryset = kwargs['queryset']
        #print('type queryset ', type(kwargs['queryset']))
        for r in kwargs['queryset']:
            #print('r ',r.related_uuid)
            for key_uuid, value_uuid in r.related_uuid.items():
                #print(f'key {key_uuid} value {value_uuid}')
                try:
                    # доедлать, с класса related.py, вставить проверку на if и отдавать связаные данные для menu
                    currentStore = StoreRelated.objects.get(Q(related_uuid__icontains=key_uuid))
                    #print('tyt')
                    if self.request.user in currentStore.store.user_permission.all():
                        #print('есть попадание по складу - ', currentStore.store.name)
                        pass
                    else:
                        #print('такого склада нет ')
                        #new_queryset = result_queryset.exclude(Q(related_uuid__icontains=key_uuid))
                        result_queryset = result_queryset.exclude(pk=r.pk)
                        #print('new_queryset ', new_queryset)
                        #result_queryset = new_queryset
                    data_uuid_related_list.append(key_uuid)
                except ObjectDoesNotExist:
                    result_queryset = result_queryset.exclude(pk=r.pk)
                    pass

        #query_list = kwargs['queryset'].values_list('related_uuid', flat=True)
        #print('result_queryset ', result_queryset)
        return result_queryset


        #conds = Q()
        #for q in data_uuid_related_list:
        #    conds |= Q(related_uuid__icontains=q)
        #if conds:
        #    result_query = Orders.objects.filter(conds).values_list('related_uuid', flat=True)

        #for query in kwargs['queryset']:
        #    print('query uuid ', query['related_uuid'])
        #if Storehouses.objects.filter(user_permission=self.request.user).exists():
        #    print('есть попадание по складу')
        #if self.request.user in Storehouses.user_permission.all():
         #   print('есть попадание по складу')

    def passCleanQueryset(self, **kwargs):
        return False