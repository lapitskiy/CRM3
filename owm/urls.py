from django.urls import path

from .views import Create, Enter, Inventory, PriceOzon, PriceWb, PriceYandex

urlpatterns = [
    path('create/', Create.as_view(), name='create'),
    path('inventory/', Inventory.as_view(), name='inventory'),
    path('price_ozon/', PriceOzon.as_view(), name='price_ozon'),
    path('price_wb/', PriceWb.as_view(), name='price_wb'),
    path('price_yandex/', PriceYandex.as_view(), name='price_yandex'),
    path('', Enter.as_view(), name='enter'),
]
