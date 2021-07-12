from django.urls import path
from .views import *

urlpatterns = [
    path('', PrintsHomeView.as_view(), name='prints_home'),
]


