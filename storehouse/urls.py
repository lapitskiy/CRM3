from django.urls import path, include
from .views import *

urlpatterns = [
    path('', StorehouseHomeViewPermit, name='storehouse_home'),
    path('settings/add/', StorehouseSettingsAddView.as_view(), name='storehouse_settings_add'),
    path('settings/edit/', StorehouseSettingsEditView.as_view(), name='storehouse_settings_edit'),
    path('settings/', StorehouseSettingsView.as_view(), name='storehouse_settings'),
]


