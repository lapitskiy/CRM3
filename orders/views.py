from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import ListView, DetailView, CreateView, FormView, TemplateView
from django.urls import reverse_lazy
from .forms import SimpleOrderAddForm, FastOrderAddForm, SettingDeviceAddForm, SettingServiceAddForm, SettingCategoryServiceAddForm, SettingStatusAddForm, SimpleOrderEditForm
from .models import Orders, Service, Device, Category_service, Status, RelatedUuid

from plugins.models import Plugins
import importlib
import shortuuid
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django.db.models import Q, F
from plugins.utils import RelatedMixin
import json
from django.forms.models import model_to_dict
import time


# from redis import Redis

from datetime import datetime, timedelta
from django.utils import timezone

class OrdersHomeView(RelatedMixin, ListView):
    #model = Orders

    paginate_by = 10
    template_name = 'orders/orders_list.html'
    context_object_name = 'orders'
    related_module_name = 'orders' #mixin

    def get_queryset(self):
        queryset = self.getQuery() #  --- 0.0 seconds ---
        orders = self.getCleanQueryset(queryset=queryset, request=self.request) #  --- 0.22246241569519043 seconds ---
        return orders

    def get_context_data(self, *, object_list=None, **kwargs):
        start_time = time.time()
        context = super(OrdersHomeView, self).get_context_data(**kwargs)
        context['title'] = 'Все заказы'
        context['filter'] = self.requestGet('filter')
        context['date'] = self.requestGet('date')
        clean_orders = self.get_queryset()
        print(f'clean_orders {type(clean_orders)}')
        #print('clean_orders', type(clean_orders)) # clean_orders <class 'django.db.models.query.QuerySet'>
        paginator = Paginator(clean_orders, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            orders_page = paginator.page(page)
        except PageNotAnInteger:
            page = 1
            orders_page = paginator.page(page)
        except EmptyPage:
            orders_page = paginator.page(paginator.num_pages)

        context['related_list'] = self.getDataListRelated(query=orders_page, method='query_paginator_page')
        context['main_list'] = list(orders_page.object_list.values('id','serial','comment', 'created_at', 'updated_at', 'status__title','status__color',
                                                                   'service__name', 'device__name', 'category_id', 'category_service__name',
                                                                   'uuid__related_uuid', 'related_user__username'))
        context['status_dict'] = self.getStatusInfo(query=clean_orders)
        #print(f" related_list {context['related_list']}")
        #print(' orders_page ', orders_page.object_list)
        #print(' =========================== ')
        #print(' dict_orders ', dict_orders)
        print(" --- %s seconds ---" % (time.time() - start_time))
        return context

    def post(self, request, *args, **kwargs):
        return super(OrdersHomeView, self).post(request, *args, **kwargs)

    def requestGet(self, req):
        if self.request.GET.get(req):
            return self.request.GET.get(req)
        else:
            return ''

    def getStatusInfo(self, query):
        dict_={}
        start_date = datetime.now() + timedelta(days=-7)
        end_date = datetime.now() + timedelta(days=-3)
        getStatus = query.filter(status__closed_status=False, created_at__range=[start_date, end_date], category__category='simple').values_list('pk', flat=True)
        #print('getStatus ', getStatus)
        dict_['warn3'] = list(getStatus)
        start_date = datetime.now() + timedelta(days=-14)
        end_date = datetime.now() + timedelta(days=-7)
        getStatus = query.filter(status__closed_status=False, created_at__range=[start_date, end_date], category__category='simple').values_list('pk', flat=True)
        #print('getStatus 2 ', getStatus)
        dict_['warn7'] = list(getStatus)
        start_date = datetime.now() + timedelta(days=-365)
        end_date = datetime.now() + timedelta(days=-14)
        getStatus = query.filter(status__closed_status=False, created_at__range=[start_date, end_date], category__category='simple').values_list('pk', flat=True)
        #print('getStatus 4 ', getStatus)
        dict_['warn14'] = list(getStatus)
        #dict_.append(getStatus)
        #getStatus = Orders.objects.filter(status__closed_status=False, category__category='simple').values_list('pk', flat=True)
        #dict_.append(getStatus)
        return dict_

    def getQuery(self):
        results_filter_uuid = []
        if self.request.GET.get('date'):
            date_get = self.request.GET.get('date')
            # ~Q(related_uuid='') |
            results_date_uuid = Orders.objects.filter(Q(created_at__icontains=date_get)).values_list('pk')

        if self.request.GET.get('filter'):
            search_query = self.request.GET.get('filter')
            # ~Q(related_uuid='') |
            results_query = Orders.objects.filter(Q(id__icontains=search_query) | Q(service__name__icontains=search_query) | Q(device__name__icontains=search_query) | Q(serial__icontains=search_query) | Q(comment__icontains=search_query)).values_list('pk', flat=True)


            uudi_filter_related_list = self.getUuidListFilterRelated(search_query)

            print('uudi_filter_related_list ', uudi_filter_related_list)

            #related_query = Orders.objects.filter(related_uuid__in=uudi_filter_related_list).values_list('related_uuid')
            conds = Q()
            for q in uudi_filter_related_list:
                conds |= Q(uuid__related_uuid=q)
            if conds:
                related_query = Orders.objects.filter(conds).values_list('pk', flat=True)
                print('related_query ', related_query)
                #conds = Q(related_uuid__in=results_query) | Q(related_uuid__in=related_query)
                #q1 = list(results_query)
                q1 = results_query
                #print('q1 ', q1)
                q2 = related_query
                #print('q2 ', q2)
                conds = Q()
                for q in q1:
                    conds |= Q(pk=q)
                for q in q2:
                    #conds |= Q(uuid__related_uuid=q)
                    conds |= Q(pk=q)
                print('conds ', conds)
                results_filter_uuid = Orders.objects.filter(conds).values_list('pk')
                print('results_filter_uuid 1 ', results_filter_uuid)
                #print('results_filter_uuid ', results_filter_uuid)
            else:
                results_filter_uuid = results_query

        print('results_filter_uuid 2 ', results_filter_uuid)

        if self.request.GET.get('date') and self.request.GET.get('filter'):
            #conds = Q(uuid__in=results_date_uuid) | Q(uuid__in=results_filter_uuid)
            conds = Q(pk__in=results_date_uuid) & Q(pk__in=results_filter_uuid)
            print('conds date and filter ', conds)
            return Orders.objects.filter(conds)
        else:
            if self.request.GET.get('filter'):
                return Orders.objects.filter(Q(pk__in=results_filter_uuid))
            else:
                if self.request.GET.get('date'):
                    return Orders.objects.filter(pk__in=results_date_uuid)
        if self.request.GET.get('category'):
            return Orders.objects.filter(category__category=self.request.GET.get('category'))
        if self.request.GET.get('status'):
            return Orders.objects.filter(status=self.request.GET.get('status'))
        return Orders.objects.all()

class OrderAddView(RelatedMixin, TemplateView):
    template_name = 'orders/order_add.html'
    related_module_name = 'orders' #relatedmixin module

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        # redis_host = '127.0.0.1'
        # r = Redis(redis_host, socket_connect_timeout=1)  # short timeout for the tes
        # r.ping()
        # print('connected to redis "{}"'.format(redis_host))

        context['forms'] = self.getRelatedFormList(request=self.request)
        formOne = self.getForm()
        formOne.prefix = 'one_form'
        context.update({'formOne': formOne})
        context.update({'tag': self.getVar()})
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        postCopy = self.ajaxConvert()
        formOne = self.getPostForm(request=self.request, postcopy=postCopy)
        related_form_dict, is_valid_related_dict = self.checkRelatedFormDict(request_post=self.request.POST, method='add', request=self.request)

        if formOne.is_valid() and is_valid_related_dict['is_valid']:
            related_uuid = shortuuid.uuid()
            form_one = formOne.save(commit=False)
            #print('form.cleaned_data', form_update.cleaned_data['category'])
            form_one.category_id = self.getCategory()
            self.increaseUsed(category_service=form_one.category_service)
            self.increaseUsed(service=form_one.service)
            self.increaseUsed(device=form_one.device)
            form_one.related_user = request.user
            make_uuid_obj = RelatedUuid(related_uuid=related_uuid)
            make_uuid_obj.save()
            form_one.save()

            form_one.uuid.add(make_uuid_obj)
            form_one.save()
            #print('self.request.GET ', self.request.GET.get('category'))
            #related form model add data
            self.saveRelatedFormData(related_form_dict=related_form_dict, request=self.request, related_uuid=related_uuid, method='add')
            '''
            for k, v  in related_form_dict.items():
                form_from_dict = related_form_dict[k]['form']
                form_add = form_from_dict.save(commit=False)
                print('form add ', form_add)
                if related_form_dict[k]['update']:
                   update_uuid_dict = related_form_dict[k]['uuid']
                   update_uuid_dict.update(related_uuid)
                   form_add.related_uuid = update_uuid_dict
                else:
                   print('related_uuid ', related_uuid)
                   form_add.related_uuid = related_uuid
                form_add.save()
                print('form save')
            '''

            return HttpResponseRedirect(reverse_lazy('orders_one', kwargs={'order_id': form_one.pk}))
        else:
            return self.form_invalid(formOne, is_valid_related_dict['form'], **kwargs)


    def ajaxConvert(self):
        postCopy = self.request.POST.copy()
        if postCopy['one_form-device']:
            try:
                pk = Device.objects.get(name=postCopy['one_form-device'])
                postCopy['one_form-device'] = pk.pk
            except ObjectDoesNotExist:
                pass
        if postCopy['one_form-service']:
            try:
                pk = Service.objects.get(name=postCopy['one_form-service'])
                postCopy['one_form-service'] = pk.pk
            except ObjectDoesNotExist:
                pass
        return postCopy

    def getVar(self):
        category_filter = self.request.GET.get('category')
        if category_filter:
            tag = category_filter
        return tag

    def getCategory(self):
        category_filter = self.request.GET.get('category')
        if category_filter == 'fast':
            return 1
        if category_filter == 'simple':
            return 2
        return 1


    def increaseUsed(self, **kwargs):
        if 'category_service' in kwargs:
            cat = Category_service.objects.get(name=kwargs['category_service'])
            cat.used = F('used') + 1
            cat.save()
        if 'service' in kwargs:
            ser = Service.objects.get(name=kwargs['service'])
            ser.used = F('used') + 1
            ser.save()
        if 'device' in kwargs:
            dev = Device.objects.get(name=kwargs['device'])
            dev.used = F('used') + 1
            dev.save()

    def getForm(self):
        category_filter = self.request.GET.get('category')
        if category_filter:
            if category_filter == 'simple':
                return SimpleOrderAddForm(request=self.request)
            if category_filter == 'fast':
                return FastOrderAddForm(request=self.request)

    def getPostForm(self, **kwargs):
        category_filter = self.request.GET.get('category')
        if category_filter:
            if category_filter == 'simple':
                return SimpleOrderAddForm(kwargs['postcopy'], request=self.request, prefix='one_form')
            if category_filter == 'fast':
                return FastOrderAddForm(kwargs['postcopy'], request=self.request, prefix='one_form')


    def form_invalid(self, formOne, form_list, **kwargs):
        context = self.get_context_data()
        formOne.prefix = 'one_form'
        #tag = 0
        #for x in form_list:
        #    x.prefix = module_list[tag]
        #    tag += 1
        context.update({'formOne': formOne})
        context['forms'] = form_list
        context['tag'] = 'fast'
        return self.render_to_response(context)

def ajax_request(request):
    """Check ajax"""
    print('tyt0')
    model = request.GET.get('model')
    method = request.GET.get('method')
    related = request.GET.get('related')
    data = request.GET.get('data')
    id = request.GET.get('id')
    if method:
        print('tyt1')
        if 'update_status' in method:
            status = request.GET.get('status')
            if status and id:
                print('tyt2')
                get_status_obj = Status.objects.get(title=status)
                Orders.objects.filter(pk=id).update(status=get_status_obj)
                response = {
                    'is_taken': 'Status update',
                    'color': get_status_obj.color,
                    'is_exist': True,
                }
                print('response ok')
            else:
                response = {
                    'is_taken': 'Status not update',
                    'is_exist': False,
                }
            return JsonResponse(response)

    if model:
        if 'service' in model:
            service = request.GET.get('one_form-service', None)
            #print('service ', service)
            qry = Service.objects.filter(Q(name__icontains=service)).values()
            qry_list = [entry for entry in qry]
            #print('qry inst', qry_list)

            if not qry or service == '':
                response = {
                    'is_taken': '',
                    'is_exist': False,
                }
            else:
                response = {
                    'is_taken': qry_list,
                    'is_exist' : True,
                }
            return JsonResponse(response)

        if 'device' in model:
            device = request.GET.get('one_form-device', None)
            #print('device', device)
            #qry = Device.objects.filter(Q(name__icontains=device)).values_list('name', flat=True)
            qry = Device.objects.filter(Q(name__icontains=device)).values()
            qry_list = [entry for entry in qry]
            #print('qry inst', qry_list)
            if not qry or device == '':
                response = {
                    'is_taken': '',
                    'is_exist': False,
                }
            else:
                response = {
                    'is_taken': qry_list,
                    'is_exist' : True,
                }
            #print('response ', response)
            return JsonResponse(response)

    """Check ajax RELATED"""

    if related and data:
        formPath = related + '.related'
        appRelated = importlib.import_module(formPath)
        related_class = appRelated.AppRelated()
        qry_list = related_class.getAjaxRelatedList(data=request.GET[data])
        #print('qry inst ', qry_list)
        if not qry_list:
            response = {
                'is_taken': '',
                'is_exist': False,
            }
        else:
            response = {
                'is_taken': qry_list,
                'is_exist' : True,
            }
        return JsonResponse(response)

class OrderEditView(RelatedMixin, TemplateView):
    template_name = 'orders/order_edit.html'

    def get(self, request, *args, **kwargs):
        start_time = time.time()
        context = super().get_context_data(**kwargs)
        get_order = Orders.objects.get(pk=context['order_id'])
        context['forms'] = self.getRelatedEditFormList(obj=get_order)
        formOne = SimpleOrderEditForm(request=self.request, instance=get_order)
        formOne.prefix = 'one_form'
        context.update({'formOne': formOne})
        print(" --- %s seconds OrderEditView ---" % (time.time() - start_time))
        return self.render_to_response(context)


    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        #related = self.checkRelated()
        #form_list = []
        #module_list = []
        #valid = True
        #flag_uuid = False
        get_order = Orders.objects.get(pk=context['order_id'])
        uuid = get_order.uuid.all()
        formOne = SimpleOrderEditForm(self.request.POST, prefix='one_form', instance=get_order, request=self.request)
        print('request ', self.request.POST)
        related_form_dict, is_valid_related_dict = self.checkRelatedFormDict(self.request.POST, method='edit', uuid=uuid)

        if formOne.is_valid() and is_valid_related_dict['is_valid']:
            formOne.save()

            self.saveRelatedFormData(related_form_dict=related_form_dict, request=self.request, related_uuid=uuid, method='edit')
            '''
            for k, v  in related_form_dict.items():
                #print('update ', related_form_dict[k]['update'])
                if not related_form_dict[k]['update']:
                    form_from_dict = related_form_dict[k]['form']
                    form_add = form_from_dict.save(commit=False)
                    form_add.uuid.add(uuid[0].pk)
                    #self.relatedDeleteMultipleUuid(dictt=related_form_dict[k], deleteUuid=uuid)
                    form_add.save()
                else:
                    form_from_dict = related_form_dict[k]['form']
                    form_add = form_from_dict.save(commit=False)
                    if related_form_dict[k]['convert']:
                        self.relatedDeleteMultipleUuid(dictt=related_form_dict[k], deleteUuid=uuid)
                        #form_add.uuid__related_uuid = uuid[0]
                    relatedClass = related_form_dict[k]['class']
                    make_uuid_obj = relatedClass.RelatedUuid(related_uuid=uuid.values_list('related_uuid', flat=True)[0])
                    make_uuid_obj.save()
                    form_add.uuid.add(ake_uuid_obj)
                    form_add.save()
            '''
            #print('Valid')
            return HttpResponseRedirect(reverse_lazy('orders_one', kwargs={'order_id': context['order_id']}))
        else:
            print('NotValid', context['order_id'])
            return self.form_invalid(formOne, is_valid_related_dict['form'], order_id=context['order_id'])

    def form_invalid(self, formOne, form_list, **kwargs):
        context = self.get_context_data()
        #context = kwargs['context']
        #print('context ', context)
        #print('order id ', context['order_id'])
        formOne.prefix = 'one_form'
        #tag = 0
        #for x in form_list:
        #    x.prefix = module_list[tag]
        #    tag += 1
        context.update({'formOne': formOne})
        context['forms'] = form_list
        context['tag'] = 'fast'
        context['order_id'] = kwargs['order_id']
        return self.render_to_response(context)

    def checkRelated(self):
        related = Plugins.objects.get(module_name='orders')
        return related.related.all()

    '''
    def get_form_class(self):
        if self.kwargs.get('tag') == 'simple':
            return SimpleOrderAddForm
        return FastOrderAddForm

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['tag'] = self.kwargs['tag']
        formOne = SimpleOrderAddForm()
        formTwo = FastOrderAddForm()
        context.update({'formOne': formOne, 'formTwo': formTwo})
        return render(request, self.template_name, context)

    

    def get_context_data(self, *, object_list=None, **kwargs):
        print('tyt')
        context = super().get_context_data(**kwargs)
        print('tyt2')
        context['tag'] = self.kwargs['tag']
        formOne = SimpleOrderAddForm()
        print('tyt')
        formTwo = FastOrderAddForm()
        print('tyt')
        print('formOne', formOne)
        context.update({'formOne': formOne, 'formTwo': formTwo})
        #context['formOne'] = SimpleOrderAddForm()
        #context['formTwo'] = FastOrderAddForm()
        return context

    def get_success_url(self):
        return reverse_lazy('orders_home')
        
    '''

class OrdersOneView(RelatedMixin, TemplateView):
    template_name = 'orders/orders_one.html'
    related_module_name = 'orders'

    def get_queryset(self, **kwargs):
        #return Orders.objects.get(pk=kwargs['id'])
        return Orders.objects.filter(pk=kwargs['id'])[0:1]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Заказ'
        order = self.get_queryset(id=context['order_id'])
        context['item'] = list(order.values('id', 'serial', 'comment', 'created_at', 'updated_at', 'status__title', 'status__color',
                                                                   'service__name', 'device__name', 'category_id', 'category_service__name',
                                                                   'uuid__related_uuid', 'related_user__username'))
        context['related_list'] = self.getDataListRelated(query=order, method='get_one_obj_by_qry')
        return context

class SettingsView(RelatedMixin, ListView):
    #model = Orders
    paginate_by = 10
    template_name = 'settings/orders_settings_list.html'
    context_object_name = 'service'

    def get_queryset(self):
        return self.getQuery()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Настройки'
        context['filter'] = self.requestGet('filter')
        # filter
        list_orders = self.getQuery()
        #paginator
        paginator = Paginator(list_orders, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            orders_page = paginator.page(page)
        except PageNotAnInteger:
            page = 1
            orders_page = paginator.page(page)
        except EmptyPage:
            orders_page = paginator.page(paginator.num_pages)

        if self.request.GET.get('model'):
            context.update({'model': self.request.GET.get('model')})
        else:
            context.update({'model': 'service'})
        #print('context ', context['model'])
        #print('context ', context)
        return context

    def post(self, request, *args, **kwargs):
        return super(OrdersSettingsView, self).post(request, *args, **kwargs)

    def requestGet(self, req):
        if self.request.GET.get(req):
            return ''
        else:
            return ''

    def getQuery(self):
        model = self.request.GET.get('model')
        filter_q = self.request.GET.get('filter')
        if model and not filter_q:
            if model == 'service':
                return Service.objects.all()
            if model == 'device':
                return Device.objects.all()
            if model == 'category_service':
                return Category_service.objects.all()
            if model == 'status':
                return Status.objects.all()

        if filter_q and model:
            if model == 'service':
                return Service.objects.filter(Q(name__icontains=filter_q))
            if model == 'device':
                return Device.objects.filter(Q(name__icontains=filter_q))
            if model == 'category_service':
                return Category_service.objects.all()
        return Service.objects.all()

    def requestGet(self, req):
        if self.request.GET.get(req):
            return self.request.GET.get('filter')
        else:
            return ''

class SettingsAddView(TemplateView):
    template_name = 'settings/settings_add.html'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        formAdd = self.getForm()
        formAdd.prefix = 'add_form'
        context.update({'formAdd': formAdd})
        context.update({'model': self.request.GET.get('model')})
        return self.render_to_response(context)


    def post(self, request, *args, **kwargs):
        formAdd = self.getPostForm(self.request.POST)
        if formAdd.is_valid():
            form_update = formAdd.save(commit=False)
            form_update.save()
            #print('Valid')
            return HttpResponseRedirect(reverse_lazy('order_settings') + '?model=' + self.request.GET.get('model'))
        else:
            #print('NotValid')
            return self.form_invalid(formAdd, **kwargs)

    def getForm(self):
        getadd = self.request.GET.get('model')
        if getadd:
            if 'service' in getadd:
                return SettingServiceAddForm
            if 'device' in getadd:
                return SettingDeviceAddForm
            if 'category_service' in getadd:
                return SettingCategoryServiceAddForm
            if 'status' in getadd:
                return SettingStatusAddForm

    def getPostForm(self, req):
        getadd = self.request.GET.get('model')
        if getadd:
            if 'service' in getadd:
                return SettingServiceAddForm(req, prefix='add_form')
            if 'device' in getadd:
                return SettingDeviceAddForm(req, prefix='add_form')
            if 'category_service' in getadd:
                return SettingCategoryServiceAddForm(req, prefix='add_form')
            if 'status' in getadd:
                return SettingStatusAddForm(req, prefix='add_form')


    def form_invalid(self, formAdd, **kwargs):
        context = self.get_context_data()
        formAdd.prefix = 'add_form'
        context.update({'formAdd': formAdd})
        context['model'] = self.request.GET.get('model')
        return self.render_to_response(context)

class SettingsEditView(TemplateView):
    template_name = 'settings/settings_edit.html'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        formEdit = self.getForm()
        formEdit.prefix = 'edit_form'
        context.update({'formEdit': formEdit})
        context.update({'model': self.request.GET.get('model')})
        context.update({'id': self.request.GET.get('id')})
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        formEdit = self.getPostForm()
        if formEdit.is_valid():
            if self.request.GET.get('model') == 'status':
                if formEdit.cleaned_data['fast_closed']:
                    dd = {'fast_closed': False}
                    Status.objects.all().update(**dd)
            formEdit.save()
            return HttpResponseRedirect(reverse_lazy('order_settings') + '?model=' + self.request.GET.get('model'))
        else:
            return self.form_invalid(formEdit, **kwargs)

    def form_invalid(self, formEdit, **kwargs):
        context = self.get_context_data()
        formEdit.prefix = 'edit_form'
        context.update({'formEdit': formEdit})
        context.update({'model': self.request.GET.get('model')})
        context.update({'id': self.request.GET.get('id')})
        return self.render_to_response(context)

    def getForm(self):
        getmodel = self.request.GET.get('model')
        if getmodel:
            if getmodel == 'service':
                get_id = Service.objects.get(pk=self.request.GET.get('id'))
                return SettingServiceAddForm(instance=get_id)
            if getmodel == 'device':
                get_id = Device.objects.get(pk=self.request.GET.get('id'))
                return SettingDeviceAddForm(instance=get_id)
            if getmodel == 'category_service':
                get_id = Category_service.objects.get(pk=self.request.GET.get('id'))
                return SettingCategoryServiceAddForm(instance=get_id)
            if getmodel == 'status':
                get_id = Status.objects.get(pk=self.request.GET.get('id'))
                return SettingStatusAddForm(instance=get_id)

    def getPostForm(self):
        getedit = self.request.GET.get('model')
        if getedit:
            if getedit == 'service':
                get_id = Service.objects.get(pk=self.request.GET.get('id'))
                return SettingServiceAddForm(self.request.POST, prefix='edit_form', instance=get_id)
            if getedit == 'device':
                get_id = Device.objects.get(pk=self.request.GET.get('id'))
                return SettingDeviceAddForm(self.request.POST, prefix='edit_form', instance=get_id)
            if getedit == 'status':
                get_id = Status.objects.get(pk=self.request.GET.get('id'))
                return SettingStatusAddForm(self.request.POST, prefix='edit_form', instance=get_id)
            if getedit == 'category_service':
                get_id = Category_service.objects.get(pk=self.request.GET.get('id'))
                return SettingCategoryServiceAddForm(self.request.POST, prefix='edit_form', instance=get_id)
