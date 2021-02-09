from django.urls import path
from .views import *

urlpatterns = [
    path('', OrdersHomeView.as_view(), name='orders_home'),
    path('orders/<int:orders_id>/', OrderCurrentView.as_view(), name='order_item'),
    path('orders/add/', OrderAddView.as_view(), name='order_add'),
]