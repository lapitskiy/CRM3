from django.urls import path
from .views import *

urlpatterns = [
    path('', ClientsHomeView.as_view(), name='clients_home'),
]


