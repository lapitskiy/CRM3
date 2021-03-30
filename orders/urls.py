from django.urls import path
from .views import *

urlpatterns = [
    path('', OrdersHomeView.as_view(), name='orders_home'),
    path('<int:order_id>/', OrderCurrentView.as_view(), name='order_item'),
    path('add/<str:tag>', OrderAddView.as_view(), name='order_add'),
    path('edit/<int:order_id>', OrderEditView.as_view(), name='order_edit'),
]