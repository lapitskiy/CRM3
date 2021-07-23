from django.urls import path, include
from .views import *

urlpatterns = [
    path('', PrintsHomeView.as_view(), name='prints_home'),
    path('add/', PrintAddView.as_view(), name='print_add'),
    path('edit/<int:print_id>', PrintEditView.as_view(), name='print_edit'),
]


