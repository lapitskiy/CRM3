from django.urls import path, include
from .views import *

urlpatterns = [
    path('', OrdersHomeView.as_view(), name='orders_home'),
    path('one/<int:order_id>', OrdersOneView.as_view(), name='orders_one'),
    path('add/', OrderAddView.as_view(), name='order_add'),
    path('edit/<int:order_id>', OrderEditView.as_view(), name='order_edit'),
    path('settings/', SettingsView.as_view(), name='order_settings'),
    path('settings/add/', SettingsAddView.as_view(), name='settings_add'),
    path('settings/edit/', SettingsEditView.as_view(), name='settings_edit'),
    path('ajax_request', ajax_request, name='ajax_request'),
]