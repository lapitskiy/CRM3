from django.views.generic import ListView
from .models import Money
from decimal import Decimal
from plugins.utils import RelatedMixin
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from .mixin import CacheQuerysetMixin

from functools import reduce
from operator import or_, and_
import operator

class MoneyHomeView(CacheQuerysetMixin, RelatedMixin, ListView):
    model = Money
    paginate_by = 10
    template_name = 'money/money_list.html'
    context_object_name = 'money'
    related_module_name = 'money'

    def get_queryset(self):
        if self._check_cached() == False:
            getQ = self._caching_queryset(self.getMoneyQuery())
        else:
            getQ = self._get_cached_queryset()
        return getQ

    def get_context_data(self, *, object_list=None, **kwargs):
        if self._check_cached() == False:
            getQ = self._caching_queryset(self.getMoneyQuery())
        else:
            #print('self._check_cached() ', self._check_cached())
            getQ = self._get_cached_queryset()
        context = super().get_context_data(**kwargs)
        context['info'] = self.getInfo(getQ)
        context['title'] = 'Деньги'
        #context['user'] = self.request.user
        #print('user ', context['user'])

        list_orders = getQ
        paginator = Paginator(list_orders, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            orders_page = paginator.page(page)
        except PageNotAnInteger:
            page = 1
            orders_page = paginator.page(page)
        except EmptyPage:
            orders_page = paginator.page(paginator.num_pages)
        #print('context info', context['info'])
        context['request'] = self.request
        #print('============================')
        #print('VIEW context', context)
        return context

    def getMoneyQuery(self):
        #print('MONEY QUERY ', self.request.GET)
        if 'rdata_' in str(self.request.GET):
            if self.request.GET.get('date'):
                date_get = self.request.GET.get('date')
            relatedListUuid = self.relatedPostGetData(request_get=self.request.GET)
            # нужно вернуть uuid по relateddata и сформировать query по Money.object
            print('relatedListUuid ', relatedListUuid)
            valuelist = []
            #intersec = None
            #query = None
            #query2 = None
            #resultquery = Money.objects.none()
            # print('MONEY QUERY 2 ', relatedListUuid)
            # print('=================================')
            # print('=================================')
            # print('=================================')
            #condition = Q()
            interslist = []
            for k, v in relatedListUuid.items():
                #print('MONEY QUERY 3')
                #Money.objects.filter(Q(related_uuid__icontains=v['relateddata']))
                #query = Money.objects.filter(reduce(and_, [Q(related_uuid__icontains=q) for q in v['relateddata']]))
                #print('query money ', query)
                if v['relateddata']:
                    #condition = Q()
                    print('1 ' , v['relateddata'])
                    # print('condition before ', condition)
                    #Companies.objects.exclusive_in('name__icontains', possible_merchants])
                    #[x for x in a if x in b]
                    interslist.append(v['relateddata'])
                    #valuelist.append(self.get_related_query_icontains(v['relateddata']))
                    #for r in v['relateddata']:
                        #condition &= Q(related_uuid__icontains=r)
                        #valuelist.append(Q(related_uuid__icontains=r))
                        #condition |= Q(related_uuid__icontains=r)
                        #valuelist.append(Q(related_uuid__icontains=r))

                        #query = Money.objects.filter(Q(related_uuid__icontains=r))
                        #resultquery = resultquery & query
                        #appendlist = Money.objects.filter(Q(related_uuid__icontains=r)).values_list('pk', flat=True)
                        #print('valuelist', valuelist)
                    # print('condition ', condition)
                    # print('=================================')

                    #valuelist.append('')
#                    valuelist.append(Money.objects.filter(condition))
            # print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
            interslist = list(set.intersection(*map(set,interslist)))
            print('interslist ', interslist)
            # print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
            #q1 = valuelist[0]
            # print('q1 ', q1)
            #q2 = valuelist[1]
            # print('q2 ', q2)
            #intersec = q1.intersection(q2)
            #print('TYT222222 ', valuelist)

            #
            #if len(valuelist) > 10:
                #print('TYT222222 ', valuelist[0])
                #for i in range(1,len(valuelist)):
                 #   intersec &= valuelist[i]

            #intersec = valuelist[0]
            #if len(valuelist) > 1:
            #    for i in range(1,len(valuelist)-1):
            #        intersec &= valuelist[i]


            #intersec = q1 & q2
            #print('intersec ', intersec)
            #print('valuelist', valuelist)
            #valuelist = self.dictUuidToList(valuelist)
            #print('valuelist', valuelist)
            #return Money.objects.filter(Q(pk__in=valuelist))
            #print('condition ', condition)
            #print('intersec ',  intersec)

            #intersec = Money.objects.filter(condition)
            #print('intersec ', intersec)
            if interslist:
                #query = Money.objects.filter(reduce(operator.and_, (Q(related_uuid__icontains=x) for x in interslist)))
                query = self.get_related_query_icontains(interslist)
                    #Money.objects.filter(reduce(and_, [Q(related_uuid__icontains=q) for q in interslist]))
                print('query money return ', query)
                return query
            else:
                print('TYT 0')
                return Money.objects.none()
            #Money.objects.filter(Q(related_uuid__icontains=interslist))
        return Money.objects.all()

    def get_related_query_icontains(self, valuelist):
        q_object = reduce(or_, (Q(related_uuid__icontains=value) for value in valuelist))
        return Money.objects.filter(q_object)

    def getInfo(self, query):
        #money
        allmoney = Decimal('0.0')
        info = {}
        for x in query:
            #print('money ', x.money)
            allmoney = allmoney + x.money
        info.update({'allmoney' : str(allmoney)})
        #order filter

        return info