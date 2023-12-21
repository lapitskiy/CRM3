from django.urls import path
from .views import *

urlpatterns = [
    path('', GoodsHomeView.as_view(), name='goods_home'),
]


