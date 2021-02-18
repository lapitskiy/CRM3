from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .forms import OrdersForm
from .models import Orders, Status

class OrdersHomeView(ListView):
    model = Orders
    template_name = 'orders/orders_list.html'
    context_object_name = 'orders'
    # extra_context = {'title': 'Главная'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Все заказы'
        return context


class OrderCurrentView(DetailView):
    model = Orders
    template_name = 'plugins/order_item.html'
    context_object_name = 'plugins_item'

class OrderAddView(CreateView):
    form_class = OrdersForm
    template_name = 'orders/order_add.html'
    #success_url = reverse_lazy('home')
    #template_name = 'news/news_detail.html'
    #pk_url_kwarg = 'news_id'

