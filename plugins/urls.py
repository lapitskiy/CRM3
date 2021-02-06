from django.urls import path
from .views import *

urlpatterns = [
    path('add-plugins/', ViewAddplugins.as_view(), name='view_add_plugins'),
    path('add-plugins/<int:pk>/', ViewCurrentAddPlugins.as_view(), name='view_current_add_plugins'),
]