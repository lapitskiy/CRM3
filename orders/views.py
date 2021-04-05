from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, FormView, TemplateView
from django.urls import reverse_lazy
from .forms import SimpleOrderAddForm, FastOrderAddForm
from .models import Orders, Status
from plugins.models import Plugins
import importlib
import shortuuid
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection




class OrdersHomeView(ListView):
    #model = Orders
    paginate_by = 10
    template_name = 'orders/orders_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return self.getQuery()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Все заказы'
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
        print('orders_page ', orders_page.object_list)
        # related data
        related = self.checkRelated()
        related_list = []
        if related:
            for x in related:
                modelPath = x.module_name + '.models'
                app_model = importlib.import_module(modelPath)
                cls = getattr(app_model, x.related_class_name)
                for r in orders_page:
                    try:
                        cls2 = cls.objects.get(related_uuid=r.related_uuid)
                        related_get = cls2.get_related_data()
                        #print('related_get', related_get)
                        related_list.append(related_get)
                    except ObjectDoesNotExist:
                        pass
        #print('related_list', related_list)
        context['related_list'] = related_list
        return context

    def checkRelated(self):
        related = Plugins.objects.get(module_name='orders')
        return related.related.all()

    def getQuery(self):
        category_filter = self.request.GET.get('category')
        if category_filter:
            list_orders = Orders.objects.filter(category__category=category_filter)
        else:
            list_orders = Orders.objects.all()
        return list_orders

class OrdersFilterView(DetailView):
    model = Orders
    template_name = 'orders/order_item.html'
    context_object_name = 'plugins_item'

class OrderAddView(TemplateView):
    template_name = 'orders/order_add.html'

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
        print('tag ', context['tag'])
        return self.render_to_response(context)


    def post(self, request, *args, **kwargs):
        formOne = self.getPostForm(self.request.POST)
        #print('formOne', formOne)
        related = self.checkRelated()
        form_list = []
        #module_list = []
        valid = True
        if related:
            for x in related:
                formPath = x.module_name + '.forms'
                app_form = importlib.import_module(formPath)
                related_form = app_form.RelatedAddForm(self.request.POST, prefix=x.module_name)
                related_form.prefix = x.module_name
                form_list.append(related_form)
                #module_list.append(x.module_name)
                if not related_form.is_valid():
                    valid = False

        if formOne.is_valid() and valid:
            related_uuid = shortuuid.uuid()
            form_update = formOne.save(commit=False)
            #print('form.cleaned_data', form_update.cleaned_data['category'])
            cat = self.getCategory()
            print('cat', cat)
            form_update.category_id = self.getCategory()
            form_update.related_uuid = related_uuid
            form_update.related_user = request.user
            print('tyt update form')
            form_update.save()
            for x in form_list:
                form_update = x.save(commit=False)
                form_update.related_uuid = related_uuid
                form_update.save()
            print('Valid')
            return HttpResponseRedirect(reverse_lazy('orders_home'))
        else:
            print('NotValid')
            return self.form_invalid(formOne, form_list, **kwargs)

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

    def checkRelated(self):
        related = Plugins.objects.get(module_name='orders')
        return related.related.all()

class OrderEditView(TemplateView):
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
                get_related = cls.objects.get(related_uuid=get_order.related_uuid)
                related_form = app_form.RelatedAddForm(instance=get_related)
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
        get_order = Orders.objects.get(pk=context['order_id'])
        formOne = SimpleOrderAddForm(self.request.POST, prefix='one_form', instance=get_order)
        if related:
            for x in related:
                formPath = x.module_name + '.forms'
                modelPath = x.module_name + '.models'
                app_form = importlib.import_module(formPath)
                app_model = importlib.import_module(modelPath)
                cls = getattr(app_model, x.related_class_name)
                get_related = cls.objects.get(related_uuid=get_order.related_uuid)
                related_form = app_form.RelatedAddForm(self.request.POST, prefix=x.module_name, instance=get_related)
                related_form.prefix = x.module_name
                form_list.append(related_form)
                #module_list.append(x.module_name)
                if not related_form.is_valid():
                    valid = False

        if formOne.is_valid() and valid:
            formOne.save()
            for x in form_list:
                x.save()
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

