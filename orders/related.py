from .models import Orders
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from plugins.utils import RelatedMixin


class AppRelated():
    prefix = 'orders'
    related_module_name = 'orders'

    # если переменная имеет возможность иметь несколько uuid на одну запись, тогда здесь идет обрабтока такой возможности
    def checkUpdate(self, **kwargs):
        return False

    # если это не создание новой модели, а изминение старой на другую уже существующую, тогда мы должены произвести смену
    # uuid мужду этими моделями
    # return False or dict uudi convert
    def checkConvert(self, **kwargs):
        return False

    def checkRelatedAddForm(self, **kwargs):
        return False

    def checkRelatedEditForm(self, **kwargs):
        return False

    def deleteRelatedMultipleUuid(self, **kwargs):
        pass

    def submenuRelated(self, **kwargs):
        context = {
            'Все заказы': 'all',
            'Быстрые заказы' : 'fast',
            'Заказы в ремонт' : 'simple'
        }
        return context

    def submenuImportRelated(self, **kwargs):
        return 'related/_related_orders_submenu.html'

    def linkGetReleatedData(self, **kwargs):
        uudi_filter_related_list = []
        if kwargs['relateddata']:
            getdata = kwargs['relateddata']
            if getdata['orders']:
                _dict = getdata['orders']
                print('dict ', _dict)
                if _dict['category'] == 'all':
                    related_result = Orders.objects.all()
                    uudi_filter_related_list = []
                    if related_result:
                        for z in related_result:
                            uudi_filter_related_list.append(z.related_uuid)
                    return uudi_filter_related_list
                if _dict['category'] == 'fast':
                    related_result = Orders.objects.filter(category__category='fast')
                    uudi_filter_related_list = []
                    if related_result:
                        for z in related_result:
                            uudi_filter_related_list.append(z.related_uuid)
                    return uudi_filter_related_list
        return uudi_filter_related_list