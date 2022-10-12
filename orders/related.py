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

    def submenuImportRelated(self, **kwargs):

        return 'related/load_sidebar_orders_related_submenu_tags.html'

    def linkGetReleatedData(self, **kwargs):
        request_get = kwargs['request_get']
        relateddata = ast.literal_eval(request_get['relateddata'])
        uudi_filter_related_list = []
        related_result = Orders.objects.none()
        cond = None
        if relateddata:
            getdata = relateddata
            logger.info('%s getdata: %s', __name__, getdata)
            if getdata['orders']:
                _dict = getdata['orders']
                if _dict['category'] == 'filterform':
                    if request_get['orders'] == 'all':
                        related_result = Orders.objects.all()
                    if request_get['orders'] == 'fast':
                        related_result = Orders.objects.filter(category__category='fast')
                    if request_get['orders'] == 'simple':
                        related_result = Orders.objects.filter(category__category='simple')
                    if request_get['date'] and request_get['date2']:
                        end_date = datetime.strptime(request_get['date2'], '%Y-%m-%d') + timedelta(days=1)
                        # print('end_date ', end_date)
                        cond = Orders.objects.filter(created_at__range=[request_get['date'],end_date])
                        related_result = related_result.intersection(cond)
                    if request_get['date'] and not request_get['date2']:
                        cond = Orders.objects.filter(Q(created_at__icontains=request_get['date']))
                        related_result = related_result.intersection(cond)
                    if not request_get['date'] and request_get['date2']:
                        cond = Orders.objects.filter(Q(created_at__icontains=request_get['date2']))
                        related_result = related_result.intersection(cond)
                    if related_result is not None:
                        logger.info('%s related_result %s', __name__, related_result)
                        for z in related_result:
                            uudi_filter_related_list.append(z.related_uuid)
                    return uudi_filter_related_list
        return uudi_filter_related_list

    def checkCleanQueryset(self, **kwargs):
        pass

    def passCleanQueryset(self, **kwargs):
        return True