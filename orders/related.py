from .models import Orders
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from plugins.utils import RelatedMixin
import ast
from datetime import datetime, timedelta


class AppRelated():
    prefix = 'orders'
    related_module_name = 'orders'
    related_format = 'data'

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
        request_get = kwargs['request_get']
        relateddata = ast.literal_eval(request_get['relateddata'])
        uudi_filter_related_list = []
        if relateddata:
            getdata = relateddata
            if getdata['orders']:
                _dict = getdata['orders']
                #print('dict ', _dict)
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
                if _dict['category'] == 'simple':
                    related_result = Orders.objects.filter(category__category='simple')
                    uudi_filter_related_list = []
                    if related_result:
                        for z in related_result:
                            uudi_filter_related_list.append(z.related_uuid)
                    return uudi_filter_related_list
                if _dict['category'] == 'date':
                    print('TYT DATE', request_get['date'])
                    print('TYT DATE 2', request_get['date2'])
                    date__range = ["2011-01-01", "2011-01-31"]
                    if request_get['date'] and request_get['date2']:
                        print('DVE DATE')
                        end_date = datetime.strptime(request_get['date2'], '%Y-%m-%d') + timedelta(days=1)
                        print('end_date ', end_date)
                        related_result = Orders.objects.filter(created_at__range=[request_get['date'],end_date])
                        #(Q(created_at__lte=request_get['date']) & Q(created_at__gte=request.POST['start_date'])
                    if request_get['date'] and not request_get['date2']:
                        print('TOLKO DATE 1')
                        related_result = Orders.objects.filter(Q(created_at__icontains=request_get['date']))
                    if not request_get['date'] and request_get['date2']:
                        print('TOLKO DATE 2')
                        related_result = Orders.objects.filter(Q(created_at__icontains=request_get['date2']))

                    uudi_filter_related_list = []
                    if related_result:
                        for z in related_result:
                            uudi_filter_related_list.append(z.related_uuid)
                    return uudi_filter_related_list
        return uudi_filter_related_list

    def checkCleanQueryset(self, **kwargs):
        pass

    def passCleanQueryset(self, **kwargs):
        return True