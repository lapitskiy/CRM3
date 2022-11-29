from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import ListView, DetailView, CreateView, FormView, TemplateView
from django.urls import reverse_lazy
from .forms import SimpleOrderAddForm, FastOrderAddForm, SettingDeviceAddForm, SettingServiceAddForm, SettingCategoryServiceAddForm, SettingStatusAddForm, SimpleOrderEditForm
from .models import Orders, Service, Device, Category_service, Status

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



class OrdersHomeView(RelatedMixin, ListView):
    #model = Orders
    paginate_by = 10
    template_name = 'orders/orders_list.html'
    context_object_name = 'orders'
    related_module_name = 'orders' #mixin

    def get_queryset(self):
        queryset = self.getQuery()
        list_orders = self.getCleanQueryset(queryset=queryset, request=self.request)
        return list_orders

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Все заказы'
        context['filter'] = self.requestGet('filter')
        context['date'] = self.requestGet('date')
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
        context['related_list'] = self.getDataListRelated(query=orders_page)
        return context

    def post(self, request, *args, **kwargs):
        return super(OrdersHomeView, self).post(request, *args, **kwargs)

    def requestGet(self, req):
        if self.request.GET.get(req):
            return self.request.GET.get('filter')
        else:
            return ''

    def getQuery(self):
        if self.request.GET.get('date'):
            date_get = self.request.GET.get('date')
            # ~Q(related_uuid='') |
            results_date_uuid = Orders.objects.filter(Q(created_at__icontains=date_get)).values_list('related_uuid')

        if self.request.GET.get('filter'):
            search_query = self.request.GET.get('filter')
            # ~Q(related_uuid='') |
            results_query = Orders.objects.filter(Q(id__icontains=search_query) | Q(service__name__icontains=search_query) | Q(device__name__icontains=search_query) | Q(serial__icontains=search_query) | Q(comment__icontains=search_query)).values_list('related_uuid')


            uudi_filter_related_list = self.getUuidListFilterRelated(search_query)

            print('uudi_filter_related_list ', uudi_filter_related_list)

            #related_query = Orders.objects.filter(related_uuid__in=uudi_filter_related_list).values_list('related_uuid')
            conds = Q()
            for q in uudi_filter_related_list:
                conds |= Q(related_uuid__icontains=q)
            if conds:
                related_query = Orders.objects.filter(conds).values_list('related_uuid', flat=True)
                print('related_query ', related_query)
                #print('related_query ', related_query)
                #print('############')
                #print('type: ',type(results_query),'results_query ', results_query)
                if related_query:
                    #conds = Q(related_uuid__in=results_query) | Q(related_uuid__in=related_query)
                    q1 = self.dictUuidToList(list(results_query))
                    #print('q1 ', q1)
                    q2 = self.dictUuidToList(list(related_query))
                    #print('q2 ', q2)
                    conds = Q()
                    for q in q1:
                        conds |= Q(related_uuid__icontains=q)
                    for q in q2:
                        conds |= Q(related_uuid__icontains=q)
                    results_filter_uuid = Orders.objects.filter(conds).values_list('related_uuid')
                    #print('results_filter_uuid ', results_filter_uuid)
            else:
                results_filter_uuid = results_query


        if self.request.GET.get('date') and self.request.GET.get('filter'):
            conds = Q(related_uuid__in=results_date_uuid) | Q(related_uuid__in=results_filter_uuid)
            return Orders.objects.filter(conds)
        else:
            if self.request.GET.get('filter'):
                return Orders.objects.filter(Q(related_uuid__in=results_filter_uuid))
            else:
                if self.request.GET.get('date'):
                    return Orders.objects.filter(Q(related_uuid__in=results_date_uuid))

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
        related_form_dict, is_valid_related_dict = self.checkRelatedFormDict(self.request.POST, doing='add', request=self.request)
        #print('related_isValid_dict', related_isValid_dict)
        #related = self.checkRelated()
        #if related:
        #    for x in related:
                #related_form = related_isValid_dict[x.module_name]['form']
                #form_list.append(related_form)
        #        if not related_isValid_dict[x.module_name]['form'].is_valid():
        #            valid = False
        #related_is_valid = self.checkRelatedIsValidDict
        #relatedValid = True # проверка связанных данных
        #for k, v in related_isValid_dict.items():
        #    if not v['valid']: relatedValid = False
        #    form_list.append(v['form'])

        if formOne.is_valid() and is_valid_related_dict['is_valid']:
            related_uuid = {shortuuid.uuid() : ''}
            form_one = formOne.save(commit=False)
            #print('form.cleaned_data', form_update.cleaned_data['category'])
            form_one.category_id = self.getCategory()
            self.increaseUsed(category_service=form_one.category_service)
            self.increaseUsed(service=form_one.service)
            self.increaseUsed(device=form_one.device)

            form_one.related_uuid = related_uuid
            form_one.related_user = request.user
            form_one.save()
            #print('related_isValid_dict ', related_form_dict)
            #related form model add data
            self.saveRelatedFormData(related_dict=related_form_dict, request=self.request, related_uuid=related_uuid)
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
    model = request.GET.get('model')
    #print('model ', model)
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
    related = request.GET.get('related')
    data = request.GET.get('data')
    #print('request.GET ', request.GET)
    #print('related ', related)
    #print('texgt ', request.GET.get('clients-phone'))
    #print('data ', data)

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
        context = super().get_context_data(**kwargs)
        get_order = Orders.objects.get(pk=context['order_id'])
        context['forms'] = self.getRelatedEditFormList(obj=get_order)
        formOne = SimpleOrderEditForm(request=self.request, instance=get_order)
        formOne.prefix = 'one_form'
        context.update({'formOne': formOne})
        return self.render_to_response(context)


    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        related = self.checkRelated()
        form_list = []
        #module_list = []
        valid = True
        flag_uuid = False
        get_order = Orders.objects.get(pk=context['order_id'])
        formOne = SimpleOrderEditForm(self.request.POST, prefix='one_form', instance=get_order, request=self.request)

        related_form_dict, is_valid_related_dict = self.checkRelatedFormDict(self.request.POST, doing='edit', uuid=get_order.related_uuid)


        #relatedValid = True
        #print('related_isValid_dict ', related_isValid_dict)
        #print('related_isValid_dict ', related_isValid_dict)
        #for k, v in related_isValid_dict.items():
        #    if not related_isValid_dict[k]['valid']:
        #        relatedValid = False

        if formOne.is_valid() and is_valid_related_dict['is_valid']:
            formOne.save()
            for k, v  in related_form_dict.items():
                #print('update ', related_form_dict[k]['update'])
                if not related_form_dict[k]['update']:
                    form_from_dict = related_form_dict[k]['form']
                    form_add = form_from_dict.save(commit=False)
                    form_add.related_uuid = get_order.related_uuid
                    self.relatedDeleteMultipleUuid(dictt=related_form_dict[k], deleteUuid=get_order.related_uuid)
                    form_add.save()
                else:
                    form_from_dict = related_form_dict[k]['form']
                    form_add = form_from_dict.save(commit=False)
                    if related_form_dict[k]['convert']:
                        self.relatedDeleteMultipleUuid(dictt=related_form_dict[k], deleteUuid=get_order.related_uuid)
                        form_add.related_uuid = related_form_dict[k]['convert']
                    form_add.save()
            #print('Valid')
            return HttpResponseRedirect(reverse_lazy('orders_home'))
        else:
            #print('NotValid', is_valid_related_dict['form'])

            return self.form_invalid(formOne, is_valid_related_dict['form'], **kwargs, order_id=context['order_id'])

    def form_invalid(self, formOne, form_list, **kwargs):
        context = self.get_context_data()
        #context = kwargs['context']
        order_id = kwargs['order_id']
        #print('context ', context)
        #print('order id ', order_id)
        formOne.prefix = 'one_form'
        #tag = 0
        #for x in form_list:
        #    x.prefix = module_list[tag]
        #    tag += 1
        context.update({'formOne': formOne})
        context['forms'] = form_list
        context['tag'] = 'fast'
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
        return Orders.objects.get(pk=kwargs['id'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Заказ'
        order = self.get_queryset(id=context['order_id'])
        context['item'] = order
        context['related_list'] = self.getDataListRelated(query=order, one='getobj')
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
            if getadd == 'service':
                return SettingServiceAddForm
            if getadd == 'device':
                return SettingDeviceAddForm
            if getadd == 'category_service':
                return SettingCategoryServiceAddForm
            if getadd == 'status':
                return SettingStatusAddForm

    def getPostForm(self, req):
        getadd = self.request.GET.get('model')
        if getadd:
            if getadd == 'service':
                return SettingServiceAddForm(req, prefix='add_form')
            if getadd == 'device':
                return SettingDeviceAddForm(req, prefix='add_form')
            if getadd == 'category_service':
                return SettingCategoryServiceAddForm(req, prefix='add_form')
            if getadd == 'status':
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
