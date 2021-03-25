from django.urls import path
from .views import *

urlpatterns = [
    path('', MoneyHomeView.as_view(), name='money_home'),
]


