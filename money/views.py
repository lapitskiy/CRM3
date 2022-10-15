from django.views.generic import ListView
from .models import Money
from decimal import Decimal
from plugins.utils import RelatedMixin
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from .mixin import CacheQuerysetMixin
from operator import and_, or_
from functools import reduce



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
            print('self._check_cached() ', self._check_cached())
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
        print('============================')
        print('VIEW context', context)
        return context

    def getMoneyQuery(self):
        print('MONEY QUERY ', self.request.GET)
        if 'rdata_' in str(self.request.GET):
            if self.request.GET.get('date'):
                date_get = self.request.GET.get('date')
            relatedListUuid = self.relatedPostGetData(request_get=self.request.GET)
            # нужно вернуть uuid по relateddata и сформировать query по Money.object
            valuelist = []
            #intersec = None
            #query = None
            #query2 = None
            #resultquery = Money.objects.none()
            # print('MONEY QUERY 2 ', relatedListUuid)
            # print('=================================')
            # print('=================================')
            # print('=================================')
            for k, v in relatedListUuid.items():
                #print('MONEY QUERY 3')
                #Money.objects.filter(Q(related_uuid__icontains=v['relateddata']))
                #query = Money.objects.filter(reduce(and_, [Q(related_uuid__icontains=q) for q in v['relateddata']]))
                #print('query money ', query)
                if v['relateddata']:
                    condition = Q()
                    # print('condition before ', condition)
                    for r in v['relateddata']:
                        condition |= Q(related_uuid__icontains=r)
                        #query = Money.objects.filter(Q(related_uuid__icontains=r))
                        #resultquery = resultquery & query
                        #appendlist = Money.objects.filter(Q(related_uuid__icontains=r)).values_list('pk', flat=True)
                        #valuelist.extend(appendlist)
                        #print('valuelist', valuelist)
                    # print('condition ', condition)
                    # print('=================================')
                    valuelist.append(Money.objects.filter(condition))
            # print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
            # print('valuelist ', valuelist)
            # print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
            q1 = valuelist[0]
            # print('q1 ', q1)
            q2 = valuelist[1]
            # print('q2 ', q2)
            #intersec = q1.intersection(q2)
            intersec = q1
            if len(valuelist) > 1:
                for i in range(1,len(valuelist)):
                    intersec &= valuelist[i]
            #intersec = q1 & q2
            #print('intersec ', intersec)
            #print('valuelist', valuelist)
            #valuelist = self.dictUuidToList(valuelist)
            #print('valuelist', valuelist)
            #return Money.objects.filter(Q(pk__in=valuelist))
            #print('condition ', condition)
            return Money.objects.filter(pk__in=intersec)
        return Money.objects.all()

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