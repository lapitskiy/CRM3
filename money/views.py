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

from datetime import datetime, timedelta

import time

class MoneyHomeView(RelatedMixin, ListView):
    paginate_by = 10
    template_name = 'money/money_list.html'
    context_object_name = 'money'
    related_module_name = 'money'

    def get_queryset(self):
        '''
        if self._check_cached() == False:
            getQ = self._caching_queryset(self.getMoneyQuery())
        else:
            getQ = self._get_cached_queryset()
        '''
        return self.getMoneyQuery()

    def get_context_data(self, *, object_list=None, **kwargs):
        start_time = time.time()
        #if self._check_cached() == False:
        #    getQ = self._caching_queryset(self.getMoneyQuery())
        #else:
            #print('self._check_cached() ', self._check_cached())
        #    getQ = self._get_cached_queryset()
        context = super(MoneyHomeView, self).get_context_data(**kwargs)
        getQ = self.getMoneyQuery()
        print('tyt11 ', type(getQ))
        print('tyt22 ', getQ)
        context['info'] = self.getInfo(getQ)
        context['title'] = 'Деньги'
        list_orders = getQ.values()
        qry_uuid_list = list(getQ.values_list('money__uuid__related_uuid', flat=True))
        print(type(getQ))
        print(getQ)
        print(type(getQ.values()))
        print(getQ.values())
        #list_orders = getQ
        #print('list_orders ', list_orders)
        #list_orders = list_orders.all()
        #print('list_orders', list_orders.all())
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
        context['related_list'] = self.getDataListRelated(query=orders_page, qry_uuid_list=qry_uuid_list, method='query_paginator_page')
        print('### money related_list ', context['related_list'])
        context['request'] = self.request
        context['get'] = self.request.GET
        #page_list = orders_page.object_list.values()
        #for x in page_list:
        #print('x ', orders_page.object_list.values())
        #test = orders_page.object_list.values()
        qry_page = orders_page
        #print('qry_page ', qry_page.object_list.values_list('pk', flat=True))
        #qry_uuid_list = list(qry.object_list.values_list('uuid__related_uuid', flat=True))
        context['money_list'] = list(qry_page.object_list.values('pk', 'id', 'prepayment', 'created_at', 'money_id'))

        #context['money_list'] = orders_page.object_list
        #getIdMoney = orders_page.object_list
        #print('money_list ', context['money_list'])
        #getPrepay = Prepayment.objects.filter()
        #print('============================')
        #print('VIEW context', context)
        print(" --- %s seconds ---" % (time.time() - start_time))
        return context

    def getMoneyQuery(self):
        #print('MONEY QUERY ', self.request.GET)
        if 'rdata_' in str(self.request.GET):
            relatedListUuid = self.relatedPostGetData(request_get=self.request.GET)
            #print('relatedListUuid ', relatedListUuid)
            interslist = []
            for k, v in relatedListUuid.items():
                if v['relateddata']:
                    interslist.append(v['relateddata'])
            #print('interslist ', interslist)
            interslist = list(set.intersection(*map(set,interslist)))
            #print('peres ', interslist)
            if interslist:
                query = self.get_related_query_icontains(interslist)
                #print('query ', query)
                return query
            else:
                #print('TYT 0')
                return Money.objects.none()
        return Prepayment.objects.none()

    def get_related_query_icontains(self, valuelist):
        q_object = reduce(or_, (Q(uuid__related_uuid=value) for value in valuelist))
        # q_object = reduce(or_, (uuid__related_uuid=value for value in valuelist))
        money_obj = Money.objects.filter(q_object)
        if self.request.GET.get('date') and not self.request.GET.get('date2'):
            date_get = self.request.GET.get('date')
            end_date = datetime.strptime(date_get, '%Y-%m-%d') + timedelta(days=1)
            date_obj = Prepayment.objects.filter(created_at__range=[date_get, end_date], money__in=money_obj)
            return date_obj
        if self.request.GET.get('date') and self.request.GET.get('date2'):
            date_get = self.request.GET.get('date')
            date2_get = self.request.GET.get('date2')
            end_date = datetime.strptime(date2_get, '%Y-%m-%d') + timedelta(days=1)
            date_obj = Prepayment.objects.filter(created_at__range=[date_get, end_date], money__in=money_obj)
            return date_obj
        return Prepayment.objects.all()

    def getInfo(self, query):
        #money
        allmoney = Decimal('0.0')
        paymoney = Decimal('0.0')
        info = {}
        for x in query:
            #print('money ', x.money)
            allmoney = allmoney + x.prepayment
            paymoney = paymoney + x.prepayment
            #paymoney = paymoney + Prepayment.get_all_prepayment_sum(id=x.money_id)
        info.update({'allmoney' : str(allmoney)})
        #info.update({'diffmoney': str(allmoney-paymoney)})
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

class MoneyEditView(RelatedMixin, TemplateView):
    template_name = 'money/money_edit.html'
    related_module_name = 'money'
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
        #print('prepayobj', context['prepayobj'])
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form_money, form_prepay = self.getPostForm(request=self.request.POST, money_id=context['money_id'])
        if self.request.GET['method'] == 'money':
            if form_money.is_valid():
                form_money.save()
            else:
                #print('tyt01')
                return self.form_invalid(form_money=form_money, form_prepay=form_prepay)
        #print('tyt0')
        if self.request.GET['method'] == 'prepay':
            if form_prepay.is_valid():
                #print('tyt1')
                form = form_prepay.save(commit=False)
                form.money_id = int(context['money_id'])
                form.save()
                #print('tyt2')
            else:
                #print('tyt3')
                return self.form_invalid(form_money=form_money, form_prepay=form_prepay)
        #print('tyt valid')
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
            print('get_form_money ', get_form_money)
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