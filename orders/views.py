from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import ListView, DetailView, CreateView, FormView, TemplateView
from django.urls import reverse_lazy
from .forms import SimpleOrderAddForm, FastOrderAddForm, SettingDeviceAddForm, SettingServiceAddForm
from .models import Orders, Service, Device

from plugins.models import Plugins
import importlib
import shortuuid
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django.db.models import Q
from plugins.utils import RelatedMixin
import json
from django.forms.models import model_to_dict




class OrdersHomeView(RelatedMixin, ListView):
    #model = Orders
    paginate_by = 10
    template_name = 'orders/orders_list.html'
    context_object_name = 'orders'
    related_module_name = 'orders'


    def get_queryset(self):
        return self.getQuery()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Все заказы'
        context['filter'] = self.requestGet('filter')
        context['date'] = self.requestGet('date')
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
        context['related_list'] = self.getDataListRelated(page=orders_page)

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
            related_query = Orders.objects.filter(conds).values_list('related_uuid', flat=True)

            print('related_query ', list(related_query))
            if related_query:
                #conds = Q(related_uuid__in=results_query) | Q(related_uuid__in=related_query)
                q1 = self.dictUuidToList(list(results_query))
                print('q1 ', q1)
                q2 = self.dictUuidToList(list(related_query))
                print('q2 ', q2)
                conds = Q()
                for q in q1:
                    conds |= Q(related_uuid__icontains=q)
                for q in q2:
                    conds |= Q(related_uuid__icontains=q)
                results_filter_uuid = Orders.objects.filter(conds).values_list('related_uuid')
                print('results_filter_uuid ', results_filter_uuid)
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
        return Orders.objects.all()

class OrderAddView(RelatedMixin, TemplateView):
    template_name = 'orders/order_add.html'
    related_module_name = 'orders' #relatedmixin module

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        related = self.checkRelated()
        if related:
            form_list = []
            for x in related:
                formPath = x.module_name + '.forms'
                app_form = importlib.import_module(formPath)
                related_form = app_form.RelatedAddForm()
                related_form.prefix = x.module_name
                form_list.append(related_form)
        context['forms'] = form_list
        #context['count_form'] = range(1, tag+1)
        formOne = self.getForm()
        formOne.prefix = 'one_form'
        context.update({'formOne': formOne})
        context.update({'tag': self.getVar()})
        return self.render_to_response(context)


    def post(self, request, *args, **kwargs):
        postCopy = self.ajaxConvert()
        formOne = self.getPostForm(postCopy)
        #print('formOne', formOne)
        form_list = []
        valid = True
        related_isValid_dict = self.checkRelatedIsValidDict(self.request.POST, doing='add') # return dict
        print('related_isValid_dict', related_isValid_dict)
        #related = self.checkRelated()
        #if related:
        #    for x in related:
                #related_form = related_isValid_dict[x.module_name]['form']
                #form_list.append(related_form)
        #        if not related_isValid_dict[x.module_name]['form'].is_valid():
        #            valid = False

        if formOne.is_valid() and not False in related_isValid_dict:
            related_uuid = {shortuuid.uuid() : ''}
            form_one = formOne.save(commit=False)
            #print('form.cleaned_data', form_update.cleaned_data['category'])
            cat = self.getCategory()
            print('cat', cat)
            form_one.category_id = self.getCategory()
            form_one.related_uuid = related_uuid
            form_one.related_user = request.user
            form_one.save()
            for k, v  in related_isValid_dict.items():
                form_from_dict = related_isValid_dict[k]['form']
                form_add = form_from_dict.save(commit=False)
                if related_isValid_dict[k]['update']:
                   update_uuid_dict = related_isValid_dict[k]['uuid']
                   update_uuid_dict.update(related_uuid)
                   form_add.related_uuid = update_uuid_dict
                else:
                   form_add.related_uuid = related_uuid
                print('form add ', form_add)
                print('erorr2? ', form_add.related_uuid)

                form_add.save()
                print('erorr3?')
            print('Valid')
            return HttpResponseRedirect(reverse_lazy('orders_home'))
        else:
            print('NotValid')
            return self.form_invalid(formOne, form_list, **kwargs)

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






        return tag

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

    def getForm(self):
        category_filter = self.request.GET.get('category')
        if category_filter:
            if category_filter == 'simple':
                return SimpleOrderAddForm
            if category_filter == 'fast':
                return FastOrderAddForm

    def getPostForm(self, req):
        category_filter = self.request.GET.get('category')
        if category_filter:
            if category_filter == 'simple':
                return SimpleOrderAddForm(req, prefix='one_form')
            if category_filter == 'fast':
                return FastOrderAddForm(req, prefix='one_form')


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
    print('model ', model)
    if model:
        if model == 'service':
            service = request.GET.get('one_form-service', None)
            print('service ', service)
            qry = Service.objects.filter(Q(name__icontains=service))
            print('qry inst', qry.values())
            if not qry or service == '':
                response = {
                    'is_taken': '',
                    'is_exist': False,
                }
            else:
                response = {
                    'is_taken': qry,
                    'is_exist' : True,
                }
            return JsonResponse(response)
        if model == 'device':
            device = request.GET.get('one_form-device', None)
            print('device', device)
            #qry = Device.objects.filter(Q(name__icontains=device)).values_list('name', flat=True)
            qry = Device.objects.filter(Q(name__icontains=device)).values()
            qry_list = [entry for entry in qry]
            print('qry inst', qry_list)
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
            print('response ', response)
            return JsonResponse(response)

class OrderEditView(RelatedMixin, TemplateView):
    template_name = 'orders/order_edit.html'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        related = self.checkRelated()
        get_order = Orders.objects.get(pk=context['order_id'])
        if related:
            form_list = []
            print('related ',related)
            for x in related:
                formPath = x.module_name + '.forms'
                modelPath = x.module_name + '.models'
                app_form = importlib.import_module(formPath)
                app_model = importlib.import_module(modelPath)
                cls = getattr(app_model, x.related_class_name)
                for key_uuid, value_uuid in get_order.related_uuid.items():
                    try:
                        get_related = cls.objects.get(Q(related_uuid__icontains=key_uuid))
                        related_form = app_form.RelatedAddForm(instance=get_related)
                    except cls.DoesNotExist:
                        related_form = app_form.RelatedAddForm()
                related_form.prefix = x.module_name
                form_list.append(related_form)
        context['forms'] = form_list
        print('form 1', context)
        formOne = SimpleOrderAddForm(instance=get_order)
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
        formOne = SimpleOrderAddForm(self.request.POST, prefix='one_form', instance=get_order)

        related_isValid_dict = self.checkRelatedIsValidDict(self.request.POST, doing='edit', uuid=get_order.related_uuid)


        relatedValid = True
        print('related_isValid_dict ', related_isValid_dict)
        for k, v in related_isValid_dict.items():
            if not related_isValid_dict[k]['valid']:
                relatedValid = False

        if formOne.is_valid() and relatedValid:
            formOne.save()
            for k, v  in related_isValid_dict.items():
                if not related_isValid_dict[k]['update']:
                    form_from_dict = related_isValid_dict[k]['form']
                    form_add = form_from_dict.save(commit=False)
                    form_add.related_uuid = get_order.related_uuid
                    self.relatedDeleteMultipleUuid(dictt=related_isValid_dict[k], deleteUuid=get_order.related_uuid)
                    form_add.save()
                else:
                    form_from_dict = related_isValid_dict[k]['form']
                    form_add = form_from_dict.save(commit=False)
                    if related_isValid_dict[k]['convert']:
                        self.relatedDeleteMultipleUuid(dictt=related_isValid_dict[k], deleteUuid=get_order.related_uuid)
                        form_add.related_uuid = related_isValid_dict[k]['convert']
                    form_add.save()
            print('Valid')
            return HttpResponseRedirect(reverse_lazy('orders_home'))
        else:
            print('NotValid')
            return self.form_invalid(formOne, form_list, **kwargs)

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
        print('1-2', model)
        if model and not filter_q:
            if model == 'service':
                print('TYT55')
                return Service.objects.all()
            if model == 'device':
                return Device.objects.all()

        if filter_q and model:
            if model == 'service':
                return Service.objects.filter(Q(name__icontains=filter_q))
            if model == 'device':
                return Device.objects.filter(Q(name__icontains=filter_q))
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
            print('Valid')
            return HttpResponseRedirect(reverse_lazy('order_settings') + '?model=' + self.request.GET.get('model'))
        else:
            print('NotValid')
            return self.form_invalid(formAdd, **kwargs)

    def getForm(self):
        getadd = self.request.GET.get('model')
        if getadd:
            if getadd == 'service':
                return SettingServiceAddForm
            if getadd == 'device':
                return SettingDeviceAddForm

    def getPostForm(self, req):
        getadd = self.request.GET.get('model')
        if getadd:
            if getadd == 'service':
                return SettingServiceAddForm(req, prefix='add_form')
            if getadd == 'device':
                return SettingDeviceAddForm(req, prefix='add_form')


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

    def getPostForm(self):
        getedit = self.request.GET.get('model')
        if getedit:
            if getedit == 'service':
                get_id = Service.objects.get(pk=self.request.GET.get('id'))
                return SettingServiceAddForm(self.request.POST, prefix='edit_form', instance=get_id)
            if getedit == 'device':
                get_id = Device.objects.get(pk=self.request.GET.get('id'))
                return SettingDeviceAddForm(self.request.POST, prefix='edit_form', instance=get_id)