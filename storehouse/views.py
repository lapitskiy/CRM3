from django.views.generic import ListView, TemplateView
from .models import Storehouses, Category
from plugins.utils import RelatedMixin
from .forms import StorehouseAddForm, StorehouseAddCategoryForm, StorehouseUserEditForm
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User, Permission


class StorehouseHomeView(ListView):
    model = Storehouses
    paginate_by = 10
    template_name = 'storehouse/storehouse_list.html'
    context_object_name = 'storehouse'
    related_module_name = 'storehouse'  # mixin

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Все склады'
        return context

StorehouseHomeViewPermit = permission_required('storehouse.view', raise_exception=True)(StorehouseHomeView.as_view())

class StorehouseSettingsAddView(RelatedMixin, TemplateView):
    template_name = 'storehouse/settings/storehouse_settings_add.html'
    related_module_name = 'storehouse' #relatedmixin module

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        formOne = self.getForm()
        formOne.prefix = 'one_form'
        context.update({'formOne': formOne})
        context.update({'tag': self.getVar()})
        return self.render_to_response(context)


    def post(self, request, *args, **kwargs):
        formOne = self.getPostForm(self.request.POST)

        if formOne.is_valid():
            form_one = formOne.save(commit=False)
            form_one.save()
            return HttpResponseRedirect(reverse_lazy('storehouse_settings'))
        else:
            print('NotValid tyt')
            print('formOne: ', formOne)
            return self.form_invalid(formOne, **kwargs)

    def getPostForm(self, req):
        category_filter = self.request.GET.get('choose')
        if category_filter:
            if category_filter == 'category':
                return StorehouseAddCategoryForm(req, prefix='one_form')
        return StorehouseAddForm(req, prefix='one_form')

    def getForm(self):
        category_filter = self.request.GET.get('choose')
        if category_filter:
            if category_filter == 'category':
                return StorehouseAddCategoryForm
        return StorehouseAddForm

    def getVar(self):
        category_filter = self.request.GET.get('category')
        if category_filter:
            tag = category_filter
            return tag
        return ''

    def form_invalid(self, formOne, **kwargs):
        context = self.get_context_data()
        formOne.prefix = 'one_form'
        context.update({'formOne': formOne})
        context['tag'] = self.request.GET.get('category')
        return self.render_to_response(context)

class StorehouseSettingsView(RelatedMixin, ListView):
    #model = Orders
    paginate_by = 10
    template_name = 'storehouse/settings/storehouse_settings_list.html'
    context_object_name = 'category'

    def get_queryset(self):
        return self.getQuery()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Настройки'
        context['show'] = self.requestGet('show')
        context['model'] = self.requestGet('model')
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
        return context

    def post(self, request, *args, **kwargs):
        return super(OrdersSettingsView, self).post(request, *args, **kwargs)

    def requestGet(self, req):
        if self.request.GET.get(req):
            return ''
        else:
            return ''

    def getQuery(self):
        if self.requestGet('show'):
            if self.request.GET.get('show') == 'category':
                return Category.objects.all()
            if self.request.GET.get('show') == 'storehouse':
                return Storehouses.objects.all()
        return ''

    def requestGet(self, req):
        if self.request.GET.get(req):
            return self.request.GET.get(req)
        else:
            return False

class StorehouseSettingsEditView(TemplateView):
    template_name = 'storehouse/settings/storehouse_settings_edit.html'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.requestGet('tag')
        context['id'] = self.requestGet('id')
        context['show'] = self.requestGet('show')
        if self.requestGet('tag') and self.requestGet('id'):
            if self.request.GET.get('tag') == 'delete':
                get_object_or_404(Category, pk=int(context['id'])).delete()
                return HttpResponseRedirect(reverse_lazy('storehouse_settings') + '?show=' + context['show'])
            if self.request.GET.get('tag') == 'edit':
                formEdit = self.getForm()
                formEdit.prefix = 'edit_form'
                context.update({'formEdit': formEdit})
                context.update({'id': self.request.GET.get('id')})
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.requestGet('tag')
        context['id'] = self.requestGet('id')
        context['show'] = self.requestGet('show')
        formEdit = self.getPostForm()
        if formEdit.is_valid():
            formEdit.save()
            return HttpResponseRedirect(reverse_lazy('storehouse_settings') + '?show=' + context['show'])
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
        getmodel = self.request.GET.get('show')
        if getmodel:
            if getmodel == 'category':
                get_id = Category.objects.get(pk=self.request.GET.get('id'))
                return StorehouseAddCategoryForm(instance=get_id)
            if getmodel == 'storehouse':
                get_id = Storehouses.objects.get(pk=self.request.GET.get('id'))
                return StorehouseAddForm(instance=get_id)

    def getPostForm(self):
        getedit = self.request.GET.get('show')
        if getedit:
            if getedit == 'category':
                print('---',self.request.GET.get('id'))
                get_id = Category.objects.get(pk=self.request.GET.get('id'))
                return StorehouseAddCategoryForm(self.request.POST, prefix='edit_form', instance=get_id)
            if getedit == 'storehouse':
                print('---',self.request.GET.get('id'))
                get_id = Storehouses.objects.get(pk=self.request.GET.get('id'))
                return StorehouseAddForm(self.request.POST, prefix='edit_form', instance=get_id)

    def requestGet(self, req):
        if self.request.GET.get(req):
            return self.request.GET.get(req)
        else:
            return False

'''
##### filter rules users
'''

# вывод правил фильтрации для пользователей
class StorehouseSettingsUsersView(RelatedMixin, ListView):
    #model = Orders
    paginate_by = 10
    template_name = 'storehouse/settings/storehouse_settings_rules.html'
    #context_object_name = 'user'

    def get_queryset(self):
        return self.getQuery()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Настройки пользователей'
        context['show'] = self.requestGet('show')
        # filter
        list_users = self.getQuery()
        #paginator
        paginator = Paginator(list_users, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            orders_page = paginator.page(page)
        except PageNotAnInteger:
            page = 1
            orders_page = paginator.page(page)
        except EmptyPage:
            orders_page = paginator.page(paginator.num_pages)
        print('context ', context)
        return context

    def requestGet(self, req):
        if self.request.GET.get(req):
            return ''
        else:
            return ''

    def getQuery(self):
        if self.requestGet('show'):
            if self.request.GET.get('show') == 'filter_rules':
                return Storehouses.objects.all()
        return ''

    def requestGet(self, req):
        if self.request.GET.get(req):
            return self.request.GET.get(req)
        else:
            return False

# редактирование правил фильтрации для пользователей
class StorehouseSettingsUsersEditView(TemplateView):
    template_name = 'storehouse/settings/storehouse_settings_rules_edit.html'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.requestGet('tag')
        context['id'] = self.requestGet('id')
        context['show'] = self.requestGet('show')
        if self.requestGet('tag') and self.requestGet('id'):
            if self.request.GET.get('tag') == 'edit':
                formEdit = self.getForm()
                formEdit.prefix = 'edit_form'
                context.update({'formEdit': formEdit})
                context.update({'id': self.request.GET.get('id')})
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.requestGet('tag')
        context['id'] = self.requestGet('id')
        context['show'] = self.requestGet('show')
        formEdit = self.getPostForm()
        if formEdit.is_valid():
            formEdit.save()
            return HttpResponseRedirect(reverse_lazy('storehouse_settings_users') + '?show=' + context['show'])
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
        get_id = Storehouses.objects.get(pk=self.request.GET.get('id'))
        return StorehouseUserEditForm(instance=get_id)

    def getPostForm(self):
        get_id = Storehouses.objects.get(pk=self.request.GET.get('id'))
        return StorehouseUserEditForm(self.request.POST, prefix='edit_form', instance=get_id)

    def requestGet(self, req):
        if self.request.GET.get(req):
            return self.request.GET.get(req)
        else:
            return False

