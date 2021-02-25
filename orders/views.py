from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .forms import FastOrderAddForm, SimpleOrderAddForm
from .models import Orders, Status

class OrdersHomeView(ListView):
    model = Orders
    paginate_by = 1
    template_name = 'orders/orders_list.html'
    context_object_name = 'orders'
    # extra_context = {'title': 'Главная'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Все заказы'
        return context

class OrderCurrentView(DetailView):
    model = Orders
    template_name = 'orders/order_item.html'
    context_object_name = 'plugins_item'

class OrderAddView(CreateView):
    template_name = 'orders/order_add.html'

    def get_form_class(self):
        if self.kwargs.get('tag') == 'simple':
            return SimpleOrderAddForm
        return FastOrderAddForm

    def get_success_url(self):
        return reverse_lazy('orders_home')
    #tag_url_kwarg = 'tag'
    #template_name = 'orders/order_add.html'
    #form_class = OrderAddForm
    #success_url = reverse_lazy('orders_home')
    #tag_url_kwarg = 'tag'
    #from_class = get_order_form(tag_url_kwarg)
    #success_url = reverse_lazy('home')
    #template_name = 'news/news_detail.html'
    #pk_url_kwarg = 'news_id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.kwargs['tag']
        print('tag ', context['tag'])
        return context