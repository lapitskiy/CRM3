from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy

from .models import Plugins, PluginsCategory

class ViewPlugins(ListView):
    model = Plugins
    template_name = 'plugins/plugins_list_view.html'
    context_object_name = 'plugins'
    # extra_context = {'title': 'Главная'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Списко плагинов'
        return context

    #def get_queryset(self):
    #    return Plugins.objects.filter(is_active=True)

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
    template_name = 'plugins/plugins_detail_view.html'
    context_object_name = 'plugins_item'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.kwargs['tag']
        return context


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
        print('context ', context)
        return context

    #def get(self, *args, **kwargs):
    #    resp = super().get(*args, **kwargs)
     #   return resp









