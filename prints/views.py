from django.views.generic import ListView, TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Prints
from plugins.utils import RelatedMixin
from .forms import SimplePrintAddForm

class PrintsHomeView(ListView):
    model = Prints
    paginate_by = 2
    template_name = 'prints/prints_list.html'
    context_object_name = 'prints'
    related_module_name = 'prints'  # mixin

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Все печатные'
        return context

class PrintFormView(RelatedMixin, TemplateView):
    template_name = 'prints/prints_form.html'
    context_object_name = 'prints'
    related_module_name = 'prints'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.GET.get('form'):
            pass
        else:
            print_form = Prints.objects.first()

        related_data = self.getDataListRelated(uuid=self.request.GET.get('uuid'), one='uuid', data='full')
        context['printform'] = self.getPrintForm(content=print_form.contentform, related=related_data)
        print('printform ', context['printform'])
        context['formnumber'] = print_form.pk
        return self.render_to_response(context)

    def getPrintForm(self, **kwargs):
        if 'content' in kwargs:
            return kwargs['content']



class PrintAddView(RelatedMixin, TemplateView):
    template_name = 'prints/print_add.html'
    related_module_name = 'prints' #relatedmixin module

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        formOne = self.getForm()
        formOne.prefix = 'one_form'
        context.update({'formOne': formOne})
        context.update({'tag': self.getVar()})
        context.update({'fields': self.relatedGetAllFieldsFromModel()})
        return self.render_to_response(context)


    def post(self, request, *args, **kwargs):
        formOne = self.getPostForm(self.request.POST)

        if formOne.is_valid():
            form_one = formOne.save(commit=False)
            form_one.save()
            return HttpResponseRedirect(reverse_lazy('prints_home'))
        else:
            print('NotValid')
            return self.form_invalid(formOne, **kwargs)

    def getPostForm(self, req):
        category_filter = self.request.GET.get('category')
        if category_filter:
            if category_filter == 'simple':
                return SimplePrintAddForm(req, prefix='one_form')

    def getForm(self):
        category_filter = self.request.GET.get('category')
        if category_filter:
            if category_filter == 'simple':
                return SimplePrintAddForm

    def getVar(self):
        category_filter = self.request.GET.get('category')
        if category_filter:
            tag = category_filter
        return tag

    def form_invalid(self, formOne, **kwargs):
        context = self.get_context_data()
        formOne.prefix = 'one_form'
        context.update({'formOne': formOne})
        context['tag'] = self.request.GET.get('category')
        return self.render_to_response(context)

class PrintEditView(RelatedMixin, TemplateView):
    template_name = 'prints/print_edit.html'
    related_module_name = 'prints' #relatedmixin module

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        get_print = Prints.objects.get(pk=context['print_id'])
        formOne = SimplePrintAddForm(instance=get_print)
        formOne.prefix = 'one_form'
        context.update({'formOne': formOne})
        context.update({'fields': self.relatedGetAllFieldsFromModel()})
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        form_list = []
        get_print = Prints.objects.get(pk=context['print_id'])
        formOne = SimplePrintAddForm(self.request.POST, prefix='one_form', instance=get_print)

        if formOne.is_valid():
            formOne.save()
            return HttpResponseRedirect(reverse_lazy('prints_home'))
        else:
            print('NotValid')
            return self.form_invalid(formOne, **kwargs)

    def form_invalid(self, formOne, **kwargs):
        context = self.get_context_data()
        formOne.prefix = 'one_form'
        context.update({'formOne': formOne})
        context['tag'] = self.request.GET.get('category')
        return self.render_to_response(context)