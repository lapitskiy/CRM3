from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .forms import RelatedPluginForm
from .models import Plugins, PluginsCategory
from plugins import settings_plugin
from .utils import RelatedMixin
import time

import importlib

class ViewPlugins(ListView):
    model = Plugins
    template_name = 'plugins/plugins_list_view.html'
    context_object_name = 'plugins'
    # extra_context = {'title': 'Главная'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Списко плагинов'
        return context


class PluginsTestView(ListView):
    model = Plugins
    template_name = 'plugins/plugins_test_view.html'
    context_object_name = 'plugins'

    # extra_context = {'title': 'Главная'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Проверка целостности приложений'
        if self.request.GET.get('error'):
            self.add_plugin_in_db(models=self.request.GET.get('models'))
        context['сountPluginDB'] = self.checkCountPluginDB()
        context['plugins_check'] = self.checkPluginStruc()
        #print('context ', context)
        return context

    def checkCountPluginDB(self, **kwargs):
        count = Plugins.objects.all().count()
        return count

    def checkPluginStruc(self, **kwargs):
        dictt = {}
        inst = []
        tag = 0
        pluginsDB_list = Plugins.objects.all().values_list('module_name', flat=True)
        pluginsDB = Plugins.objects.all()
        for k in settings_plugin.INSTALLED_APPS_ADD:
            z = k[0: k.find('.')]
            inst.append(z)
            if z not in pluginsDB_list:
                dict2 = {}
                dict2['models'] = z
                dict2['text'] = 'Отсуствует запись в DB, приложение указано только в INI файле'
                dict2['err'] = 'dberror'
                tag += 1
                dictt[tag] = dict2
        for t in pluginsDB:
            if t.module_name not in inst:
                dict2 = {}
                dict2['models'] = t.module_name
                dict2['text'] = 'Отсуствует запись в INI, приложение указано только в DB файле'
                dict2['err'] = 'inierror'
                tag += 1
                dictt[tag] = dict2
        return dictt

    def add_plugin_in_db(self, **kwargs):
        if 'models' in kwargs:
            models = kwargs['models']
            cfgPath = models + '.install'
            cfg_lib = importlib.import_module(cfgPath)
            cfg = cfg_lib.REPO_DATA
            Plugins.objects.update_or_create(title=cfg['title'], module_name=cfg['module_name'], description=cfg['description'], version=cfg['version'], related_class_name=cfg['related_class_name'])
    #def get_queryset(self):
    #    return Plugins.objects.filter(is_active=True)

class PluginsUuidUpdateView(RelatedMixin, ListView):
    model = Plugins
    template_name = 'plugins/plugins_uuid_view.html'
    context_object_name = 'plugins'

    # extra_context = {'title': 'Главная'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'перенос uuid из версии v1 в версию v2'

        #context['resultUuid'] = self.checkUuid()
        #print('context ', context)
        return context

    @classmethod
    def checkUuid(self, **kwargs):
        start_time = time.time()
        #related = self.checkRelated()
        dict_ = {}
        module = Plugins.objects.all().values('module_name', 'related_class_name')
        for iterr in module:
            #print('key val ', iterr)
            modelPath = iterr['module_name'] + '.models'
            imp_model = importlib.import_module(modelPath)
            cls_model = getattr(imp_model, iterr['related_class_name'])
            cls_relateduuid = getattr(imp_model, 'RelatedUuid')

            obj_ = cls_model.objects.all()
            print('go ', iterr['module_name'], ' ; count: ', len(obj_))
            for item in obj_:
                related_json = item.related_uuid
                #for item in obj:
                #print('item: ', obj)
                #dict_2 = obj['related_uuid']

                #print('dict_2: ', dict_2)
                #print('type: ', type(dict_2))
                #p = Person.objects.create(first_name="Bruce", last_name="Springsteen")
                if type(related_json) is dict:
                    if len(related_json) > 1:
                        for key in related_json.keys():
                            related_uuid = cls_relateduuid.objects.update_or_create(related_uuid=key)
                            item.uuid.add(related_uuid[0])
                            item.save()
                            #related_uuid.cls_model_set.add(item)
                            #item.uuid_set.create(related_uuid=key)
                    else:
                        for key, value in related_json.items():
                            #print('long uuid ', len(key), key)
                            related_uuid = cls_relateduuid.objects.update_or_create(related_uuid=key)
                            item.uuid.add(related_uuid[0])
                            item.save()

        dict_['time'] = time.time() - start_time
        return dict_

def ajax_request(request):
    """Check ajax"""
    print('ajax')
    response = PluginsUuidUpdateView.checkUuid()
    return JsonResponse(response)


class ViewPluginsByCategory(ListView):
    model = Plugins
    template_name = 'plugins/plugins_list.html'
    context_object_name = 'plugins'
    allow_empty = False
    # extra_context = {'title': 'Главная'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = PluginsCategory.objects.get(pk=self.kwargs['id'])
        return context

    def get_queryset(self):
        return Plugins.objects.filter(is_published=True, category=self.kwargs['id'])


class ViewCurrentPlugins(DetailView):
    model = Plugins
    context_object_name = 'plugins'
    template_name = 'plugins/plugins_detail_view.html'
    context_object_name = 'plugins_item'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.kwargs['tag']
        context['form'] = RelatedPluginForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)

        form = RelatedPluginForm(request.POST)
        related_id = request.POST['related']
        context['form'] = form
        #print('request.POST', request.POST)
        #print('related_id', related_id)

        if form.is_valid():
            self.plugin = self.get_object()
            if 'related_add' in request.POST:
                self.plugin.related.add(related_id)
            elif 'related_del' in request.POST:
                self.plugin.related.remove(related_id)
            self.plugin.save()
            return self.render_to_response(context=context)
        else:
            return self.render_to_response(context=context)

###
### VIEW GLOBAL PLUGIN
###

class ViewRepositoryPlugins(ListView):
    model = Plugins
    template_name = 'plugins/repository_list.html'
    context_object_name = 'plugins'

    # extra_context = {'title': 'Главная'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Списко плагинов'

        #context['link'] = request.path
        #print('context ', context)
        return context

    def get_queryset(self):
        return Plugins.objects.filter(is_active=True)

class InstallRepositoryPlugins(ListView):
    model = Plugins
    template_name = 'plugins/install_plugin.html'
    context_object_name = 'plugins'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Установка плагина'
        context['id']= self.kwargs['id']
        context['tag'] = self.kwargs['tag']
        #context['link'] = request.path
        #print('context ', context)
        return context

    #def get(self, *args, **kwargs):
    #    resp = super().get(*args, **kwargs)
     #   return resp









