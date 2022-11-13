from django.urls import path
from .views import *

urlpatterns = [
    path('', MoneyHomeView.as_view(), name='money_home'),
    path('edit/<int:money_id>', MoneyEditView.as_view(), name='money_edit'),
]


