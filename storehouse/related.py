from .forms import RelatedAddForm
from .models import Storehouses
from django.db.models import Q

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
        return True

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
        #print('request clients-phone checkRelatedAddForm: ', request_post['clients-phone'])
        #print('checkUpdate ', self.checkUpdate(request_post=request_post))
        if self.checkUpdate(request_post=request_post):
            pass
        else:
            related_form = RelatedAddForm(request_post, prefix=self.prefix)
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
