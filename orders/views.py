from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, FormView, TemplateView
from django.urls import reverse_lazy
from .forms import SimpleOrderAddForm, FastOrderAddForm
from .models import Orders
from plugins.models import Plugins
import importlib
import shortuuid
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django.db.models import Q




class OrdersHomeView(ListView):
    #model = Orders
    paginate_by = 10
    template_name = 'orders/orders_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return self.getQuery(self.checkRelated())

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Все заказы'
        context['filter'] = self.requestGet('filter')
        context['date'] = self.requestGet('date')
        # filter
        related = self.checkRelated()
        list_orders = self.getQuery(related)
        print('list_orders ', list_orders)
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
        # related data
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

    def post(self, request, *args, **kwargs):
        print('EEE')
        print('self 2', self.request.POST['csrfmiddlewaretoken'])
        return super(OrdersHomeView, self).post(request, *args, **kwargs)


    def checkRelated(self):
        related = Plugins.objects.get(module_name='orders')
        return related.related.all()

    def requestGet(self, req):
        if self.request.GET.get(req):
            return self.request.GET.get('filter')
        else:
            return ''

    def getQuery(self, related):
        if self.request.GET.get('date'):
            date_get = self.request.GET.get('date')
            # ~Q(related_uuid='') |
            results_date_uuid = Orders.objects.filter(Q(created_at__icontains=date_get)).values_list('related_uuid')

        if self.request.GET.get('filter'):
            search_query = self.request.GET.get('filter')
            # ~Q(related_uuid='') |
            results_query = Orders.objects.filter(Q(device__icontains=search_query) | Q(serial__icontains=search_query) | Q(
                    comment__icontains=search_query)).values_list('related_uuid')
            list_related = []
            if related:
                for x in related:
                    modelPath = x.module_name + '.models'
                    app_model = importlib.import_module(modelPath)
                    cls = getattr(app_model, x.related_class_name)
                    #search_query = {'search_query' : search_query}
                    #r_cls = cls()
                    related_result = cls().get_related_filter(search_query=search_query)
                    if related_result:
                        for z in related_result:
                            list_related.append(z.related_uuid)
            print('list_related', list_related)
            related_query = Orders.objects.filter(related_uuid__in=list_related).values_list('related_uuid')
            print('related_query', related_query)
            #related_conds = list_related_conds[0]
            #for x in list_related_conds[1:]:
            #    related_conds = related_conds | x
            #print('related_conds 3', related_conds)
            if related_query:
                #conds = Q(related_uuid__icontains=results_query) | Q(related_uuid__icontains=related_query)
                conds = Q(related_uuid__in=results_query) | Q(related_uuid__in=related_query)
                print('try cond if', conds)
                results_filter_uuid = Orders.objects.filter(conds).values_list('related_uuid')
            else:
                print('try cond else')
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
                try:
                    get_related = cls.objects.get(related_uuid=get_order.related_uuid)
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
        if related:
            for x in related:
                formPath = x.module_name + '.forms'
                modelPath = x.module_name + '.models'
                app_form = importlib.import_module(formPath)
                app_model = importlib.import_module(modelPath)
                cls = getattr(app_model, x.related_class_name)

                try:
                    get_related = cls.objects.get(related_uuid=get_order.related_uuid)
                    related_form = app_form.RelatedAddForm(self.request.POST, prefix=x.module_name,
                                                           instance=get_related)
                except cls.DoesNotExist:
                    related_form = app_form.RelatedAddForm(self.request.POST, prefix=x.module_name)
                    flag_uuid = True
                related_form.prefix = x.module_name
                form_list.append(related_form)
                #module_list.append(x.module_name)
                if not related_form.is_valid():
                    valid = False

        if formOne.is_valid() and valid:
            formOne.save()
            for x in form_list:
                if flag_uuid:
                    form_update = x.save(commit=False)
                    form_update.related_uuid = get_order.related_uuid
                    form_update.save()
                else:
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

