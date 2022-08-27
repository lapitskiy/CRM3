from django.views.generic import ListView
from .models import Money
from decimal import Decimal
from plugins.utils import RelatedMixin
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

class MoneyHomeView(RelatedMixin, ListView):
    model = Money
    paginate_by = 10
    template_name = 'money/money_list.html'
    context_object_name = 'money'
    related_module_name = 'money'

    def get_queryset(self):
        return self.getQuery()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['info'] = self.getInfo(self.getQuery())
        context['title'] = 'Деньги'
        list_orders = self.get_queryset()
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
        return context

    def getQuery(self):
        if self.request.GET.get('relateddata'):
            if self.request.GET.get('date'):
                date_get = self.request.GET.get('date')

            relatedListUuid = self.relatedPostGetData(request_get=self.request.GET)
            # нужно вернуть uuid по relateddata и сформировать query по Money.object
            print('relatedListUuid', relatedListUuid)
            valuelist = []
            for k, v in relatedListUuid.items():
                for r in v['relateddata']:
                    appendlist = Money.objects.filter(Q(related_uuid__icontains=r)).values_list('pk', flat=True)
                    valuelist.extend(appendlist)
                    #print('valuelist', valuelist)
            #print('valuelist', valuelist)
            #valuelist = self.dictUuidToList(valuelist)
            #print('valuelist', valuelist)
            return Money.objects.filter(Q(pk__in=valuelist))
        return Money.objects.all()

    def getInfo(self, query):
        allmoney = Decimal('0.0')
        context = {}
        for x in query:
            #print('money ', x.money)
            allmoney = allmoney + x.money

        context.update({'allmoney' : str(allmoney)})
        return context