from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, FormView, TemplateView
from django.urls import reverse_lazy
from .forms import FastOrderAddForm, SimpleOrderAddForm
from .models import Orders, Status
from plugins.models import Plugins
import importlib
import shortuuid
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger




class OrdersHomeView(ListView):
    model = Orders
    paginate_by = 2
    template_name = 'orders/orders_list.html'
    context_object_name = 'orders'
    # extra_context = {'title': 'Главная'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Все заказы'

        list_orders = Orders.objects.all()
        paginator = Paginator(list_orders, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            orders_page = paginator.page(page)
        except PageNotAnInteger:
            page = 1
            orders_page = paginator.page(page)
        except EmptyPage:
            orders_page = paginator.page(paginator.num_pages)
        print('paginator', orders_page.object_list)

        # related data
        related = self.checkRelated()
        if related:
            related_uuid = []
            for x in related:
                modelPath = x.module_name + '.models'
                app_model = importlib.import_module(modelPath)
                cls = getattr(app_model, x.related_class_name)
                print('cls', cls)
                for r in orders_page:
                    related_uuid.append(cls.objects.filter(related_uuid=r.related_uuid))
        context['related_uuid'] = related_uuid
        return context

    def checkRelated(self):
        related = Plugins.objects.get(module_name='orders')
        return related.related.all()

class OrderCurrentView(DetailView):
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
            print('related ',related)
            for x in related:
                formPath = x.module_name + '.forms'
                app_form = importlib.import_module(formPath)
                related_form = app_form.RelatedAddForm()
                related_form.prefix = x.module_name
                form_list.append(related_form)
        context['forms'] = form_list
        #context['count_form'] = range(1, tag+1)
        print('form ', context)
        formOne = SimpleOrderAddForm()
        formOne.prefix = 'one_form'
        context.update({'formOne': formOne})
        return self.render_to_response(context)


    def post(self, request, *args, **kwargs):
        formOne = SimpleOrderAddForm(self.request.POST, prefix='one_form')
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
            form_update.related_uuid = related_uuid
            form_update.save()
            for x in form_list:
                form_update = x.save(commit=False)
                form_update.related_uuid = related_uuid
                form_update.save()
            print('Valid')
            return HttpResponseRedirect('orders_home')
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

