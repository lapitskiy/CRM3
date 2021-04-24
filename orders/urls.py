from django.urls import path
from .views import *

urlpatterns = [
    path('', OrdersHomeView.as_view(), name='orders_home'),
    path('add/', OrderAddView.as_view(), name='order_add'),
    path('edit/<int:order_id>', OrderEditView.as_view(), name='order_edit'),
    path('ajax_request', ajax_request, name='ajax_request')

]