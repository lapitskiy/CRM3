from django.views.generic import ListView, TemplateView
from .models import Prints
from plugins.utils import RelatedMixin
from .forms import SimplePrintAddForm

class PrintsHomeView(ListView):
    model = Prints
    paginate_by = 2
    template_name = 'prints/prints_list.html'
    context_object_name = 'prints'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Все печатные'
        return context

class PrintAddView(RelatedMixin, TemplateView):
    template_name = 'prints/print_add.html'
    related_module_name = 'prints' #relatedmixin module

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        related = self.checkRelated()
        form_list = []
        if related:
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