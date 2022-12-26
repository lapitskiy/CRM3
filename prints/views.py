from django.views.generic import ListView, TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Prints
from plugins.utils import RelatedMixin
from .forms import SimplePrintAddForm
import re
import importlib

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
        #related_data = self.getDataListRelated(uuid=self.request.GET.get('uuid'), method='get_one_obj_by_str_uuid', data='dict')
        #print('related_data prints ', related_data)
        context['printform'] = self.getPrintForm(content=print_form.contentform)
        context['formnumber'] = print_form.pk
        return self.render_to_response(context)

    def getPrintForm(self, **kwargs):
        after_text = ''
        #print('related ', kwargs['related'])
        #print('print_form.contentform ', kwargs['content'])
        #related = kwargs['related']
        #print('kwargs rel', related)
        #rel_money = related[0]['money']
        #print('kwargs', rel_money)
        if 'content' in kwargs:
            #list_related = re.findall(r'[a-zA-Z0-9]+\.[a-zA-Z0-9]+\.[a-zA-Z0-9]+', kwargs['content'])
            after_text = kwargs['content']
            list_related = [f.group(0) for f in re.finditer('(?<={{)(.*?)(?=}})', kwargs['content'])]

            for x in list_related:
                list_split = x.split('.')
                get_obj = self.getModelFromStr(uuid=self.request.GET.get('uuid'), app=list_split[0], cls=list_split[1])
                #print('split 2: ', list_split[2])
                #print('get_obj: ', get_obj)
                if get_obj:
                    get_name = getattr(get_obj, list_split[2])
                    after_text = after_text.replace('{{'+x+'}}', str(get_name))
                else:
                    after_text = after_text.replace('{{'+x+'}}', 'не указано')

        return after_text

    # [EN] return obj
    # [RU] возвращает объект на основе строк класса и app
    def getModelFromStr(self, **kwargs):
        if 'cls' in kwargs and 'app' in kwargs and 'uuid' in kwargs:
            modelPath = kwargs['app'] + '.models'
            imp_model = importlib.import_module(modelPath)
            cls_model = getattr(imp_model, kwargs['cls'])
            try:
                cls2 = cls_model.objects.get(uuid__related_uuid=kwargs['uuid'])
                return cls2
            except cls_model.DoesNotExist:  # тоже самое с cls2.DoesNotExist:
                return False
        return False


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