from .models import Orders
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from plugins.utils import RelatedMixin
import ast
from datetime import datetime, timedelta

import logging

logger = logging.getLogger('crm3_info')


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

    def submenuImportRelated(self, **kwargs) -> str:
        return 'related/load_sidebar_orders_related_submenu_tags.html'

    def linkGetReleatedData(self, **kwargs) -> dict:
        request_get = kwargs['request_get']
        relateddata = ast.literal_eval(request_get['rdata_orders'])
        uudi_filter_related_list = []
        query = None
        query2 = None #Orders.objects.none()
        # cond = None
        if relateddata:
            getdata = relateddata
            logger.info('%s getdata: %s', __name__, getdata)
            if 'submenu' in getdata:
                _dict = getdata['submenu']
                if _dict['category'] == 'filterform':
                    if request_get['orders'] == 'all':
                        query = Orders.objects.all()
                    if request_get['orders'] == 'fast':
                        query = Orders.objects.filter(category__category='fast')
                    if request_get['orders'] == 'simple':
                        query = Orders.objects.filter(category__category='simple')
                    if request_get['date'] and request_get['date2']:
                        #print('DATE 1')
                        end_date = datetime.strptime(request_get['date2'], '%Y-%m-%d') + timedelta(days=1)
                        # print('end_date ', end_date)
                        query2 = Orders.objects.filter(created_at__range=[request_get['date'],end_date])
                    if request_get['date'] and not request_get['date2']:
                        #print('DATE 2')
                        #date = datetime.strptime(request_get['date'], '%Y-%m-%d') + timedelta(days=1)

                        #query2 = Orders.objects.filter(Q(created_at__icontains=date))
                        #date = datetime.strptime(request_get['date'], '%Y-%m-%d')
                        end_date = datetime.strptime(request_get['date'], '%Y-%m-%d') + timedelta(days=1)
                        query2 = Orders.objects.filter(created_at__range=[request_get['date'],end_date])
                    if not request_get['date'] and request_get['date2']:
                        #print('DATE 3')
                        query2 = Orders.objects.filter(Q(created_at__icontains=request_get['date2']))
                    if query is not None:
                        #print('q1 ', query)
                        #print('q2 ', query2)
                        if query2 is not None:
                            #print('query ', query)
                            #print('query 2', query2)
                            query = query & query2
                            #print('query result ', query)
                        #logger.info('%s related_result %s', __name__, type(intersection))
                        #print('intersection ', intersection)
                        for z in query:
                            uuid = z.uuid.all().values_list('related_uuid', flat=True)
                            try:
                                uudi_filter_related_list.append(uuid[0])
                            except IndexError:
                                pass
                    return uudi_filter_related_list
        return uudi_filter_related_list

    def checkCleanQueryset(self, **kwargs):
        pass

    def passCleanQueryset(self, **kwargs):
        return True