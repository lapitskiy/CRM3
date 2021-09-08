from django.urls import path, include
from .views import *

urlpatterns = [
    path('', StorehouseHomeView.as_view(), name='storehouse_home'),
    path('', StorehouseAddView.as_view(), name='storehouse_add'),
    path('settings/', StorehouseSettingsView.as_view(), name='storehouse_settings'),
]


