from django.views.generic import ListView, TemplateView, FormView
from .models import Money, Prepayment
from .forms import MoneyEditForm, PrepayEditForm
from decimal import Decimal
from plugins.utils import RelatedMixin
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from .mixin import CacheQuerysetMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from functools import reduce
from operator import or_, and_

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
                print('!related! ', v['relateddata'])
                if v['relateddata']:
                    #condition = Q()
                    #print('1 ' , v['relateddata'])
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
            for x in interslist:
                print('interslist x ', x)
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
        paymoney = Decimal('0.0')
        info = {}
        for x in query:
            #print('money ', x.money)
            allmoney = allmoney + x.money
            #paymoney = paymoney + x.prepayment
        info.update({'allmoney' : str(allmoney)})
        info.update({'paymoney': str(paymoney)})
        return info

'''
class MoneyEditViewTEST(FormView):
    form_money = MoneyEditForm
    form_prepay = PrepayEditForm
    template_name = 'money/money_edit.html'
    #success_url = HttpResponseRedirect(reverse_lazy('money_edit', kwargs={'money_id': context['money_id']}))
    extra_context = {
        'money_id': context['money_id'],
    }

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        form_money, form_prepay = self.getForm(id=context['money_id'])
        context.update({'form_money': form_money})
        context.update({'form_prepay': form_prepay})
        context.update({'id': context['money_id']})
        context.update({'moneyobj': Money.objects.get(pk=context['money_id'])})
        try:
            get_moneyobj = Money.objects.get(pk=context['money_id'])
            context.update({'moneyobj': get_moneyobj})
            context.update({'prepayobj': Prepayment.objects.get(money=context['money_id'])})
        except Money.DoesNotExist:
            raise Http404
        except Prepayment.DoesNotExist:
            pass
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        form_money, form_prepay = self.getPostForm(request=self.request.POST, id=context['money_id'])
        print('context1: ', context)
        if form_money.is_valid():
            form_money.save()
        else:
            return self.form_invalid(form_money)

        if form_prepay.is_valid():
            form_prepay.save()
        else:
            return self.form_invalid(form_prepay)

    def form_invalid(self, form, **kwargs):
        context = self.extra_context
        print('context ext: ', context)
        context = self.get_context_data(**kwargs)
        if form.prefix == 'form_prepay':
            context.update({'form_prepay': form})
        if form.prefix == 'form_money':
            context.update({'form_money': form})
        context.update({'id': self.request.GET.get('id')})
        #context.update({'money_id': self.request.GET.get('id')})
        context.update({'money_id': context['money_id']})
        print('context: ', context)
        return self.render_to_response(context)

    def getForm(self, **kwargs):
        getid = kwargs['id']
        if getid:
            try:
                get_moneyobj = Money.objects.get(pk=getid)
                get_inst_money = MoneyEditForm(instance=get_moneyobj)
                get_inst_money.prefix = 'form_money'
                #get_prepayobj = Prepayment.objects.get(money=getid)
            except Money.DoesNotExist:
                raise Http404
            #except Prepayment.DoesNotExist:
            #    get_inst_prepay = PrepayEditForm()
            #    get_inst_prepay.prefix = 'form_prepay'
            #    return get_inst_money, get_inst_prepay
            #for x in get_prepayobj:
            #    get_inst_prepay = PrepayEditForm(instance=get_prepayobj)
            #    get_inst_prepay.prefix = 'form_prepay'
            get_inst_prepay = PrepayEditForm()
            get_inst_prepay.prefix = 'form_prepay'
            return get_inst_money, get_inst_prepay

    def getPostForm(self, **kwargs):
        getid = kwargs['id']
        if getid:
            get_moneyobj = Money.objects.get(pk=getid)
            get_form_money = MoneyEditForm(self.request.POST, prefix='form_money', instance=get_moneyobj)
            get_form_prepay = PrepayEditForm(self.request.POST, prefix='form_prepay')
            try:
                get_prepayobj = Prepayment.objects.get(money=getid)
                sum_ = get_prepayobj.getPrepaySum()
                #sum_ = sum([x.prepayment for x in get_prepayobj])
                #sum = 0
                #for x in get_prepayobj:
                #    sum += x.prepayment
                print('self.request.POST ', self.request.POST)
                if sum_+Decimal(self.request.POST['form_prepay-prepayment']) > get_moneyobj.money:
                    #form_prepay - prepayment
                    get_form_prepay.add_error('prepayment', 'предоплата выше, чем текущая стоимость')
            except Prepayment.DoesNotExist:
                print('self.request.POST 2', self.request.POST)
                if 'form_prepay-prepayment' in self.request.POST:
                    print('tyt')
                    if Decimal(self.request.POST['form_prepay-prepayment']) > get_moneyobj.money:
                        print('tyt2')
                        get_form_prepay.add_error('prepayment', 'предоплата выше, чем текущая стоимость')
            print('get_form_prepay ', get_form_prepay)
            return get_form_money, get_form_prepay
'''

class MoneyEditView(TemplateView):
    template_name = 'money/money_edit.html'
    #extra_context = {'money_id':}

    def get_context_data(self, **kwargs):
        context = super(MoneyEditView, self).get_context_data(**kwargs)
        context.update({
            'money_id': self.kwargs.get('money_id', None),
        })
        dict_ = self.getObj(self.kwargs.get('money_id', None))
        context.update(dict_)
        return context

    def getObj(self, money_id):
        try:
            get_moneyobj = Money.objects.get(pk=money_id)
            dict_ = {}
            dict_.update({'moneyobj': get_moneyobj})
            dict_.update({'prepayobj': Prepayment.objects.filter(money=money_id)})
            dict_.update({'prepay_sum': Prepayment.get_all_prepayment_sum(id=money_id)})
            if dict_['prepay_sum'] is None:
                dict_['prepay_sum'] = Decimal('0.0')
        except Money.DoesNotExist:
            raise Http404
        except Prepayment.DoesNotExist:
            pass
        return dict_

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form_money, form_prepay = self.getForm(id=context['money_id'])
        context.update({'form_money': form_money})
        context.update({'form_prepay': form_prepay})
        print('prepayobj', context['prepayobj'])
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form_money, form_prepay = self.getPostForm(request=self.request.POST, money_id=context['money_id'])
        #print('context1: ', context)
        if form_money.is_valid():
            form_money.save()
        else:
            return self.form_invalid(form_money=form_money, form_prepay=form_prepay)

        if form_prepay.is_valid():
            form = form_prepay.save(commit=False)
            form.money_id = int(context['money_id'])
            form.save()
        else:
            return self.form_invalid(form_money=form_money, form_prepay=form_prepay)
        print('tyt valid')
        return HttpResponseRedirect(reverse_lazy('money_edit', kwargs={'money_id': context['money_id']}))

    def form_invalid(self, **kwargs):
        context = self.get_context_data(**kwargs)
        form_prepay = kwargs['form_prepay']
        form_money = kwargs['form_money']
        context.update({'form_prepay': form_prepay})
        context.update({'form_money': form_money})
        return self.render_to_response(context)

    def getForm(self, **kwargs):
        getid = kwargs['id']
        if getid:
            try:
                get_moneyobj = Money.objects.get(pk=getid)
                get_inst_money = MoneyEditForm(instance=get_moneyobj)
                get_inst_money.prefix = 'form_money'
                #get_prepayobj = Prepayment.objects.get(money=getid)
            except Money.DoesNotExist:
                raise Http404
            #except Prepayment.DoesNotExist:
            #    get_inst_prepay = PrepayEditForm()
            #    get_inst_prepay.prefix = 'form_prepay'
            #    return get_inst_money, get_inst_prepay
            #for x in get_prepayobj:
            #    get_inst_prepay = PrepayEditForm(instance=get_prepayobj)
            #    get_inst_prepay.prefix = 'form_prepay'
            get_inst_prepay = PrepayEditForm()
            get_inst_prepay.prefix = 'form_prepay'
            return get_inst_money, get_inst_prepay

    def getPostForm(self, **kwargs):
        context = self.get_context_data(**kwargs)
        getid = kwargs['money_id']
        if getid:
            get_moneyobj = Money.objects.get(pk=getid)
            get_form_money = MoneyEditForm(self.request.POST, prefix='form_money', instance=get_moneyobj)
            get_form_prepay = PrepayEditForm(self.request.POST, prefix='form_prepay')
            #try:
                #get_prepayobj = Prepayment.objects.filter(money=getid)
                #sum_ = get_prepayobj.getPrepaySum()

                #sum_ = sum([x.prepayment for x in get_prepayobj])
                #sum = 0
                #for x in get_prepayobj:
                #    sum += x.prepayment
                #print('self.request.POST ', self.request.POST)
            if 'form_prepay-prepayment' in self.request.POST:
                if context['prepay_sum']+Decimal(self.request.POST['form_prepay-prepayment']) > get_moneyobj.money:
                    #form_prepay - prepayment
                    get_form_prepay.add_error('prepayment', 'предоплата выше, чем текущая стоимость')
                #except Prepayment.DoesNotExist:
                    #print('self.request.POST 2', self.request.POST)
                #print('get_form_prepay ', get_form_prepay)
            return get_form_money, get_form_prepay