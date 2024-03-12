from django.urls import path

from .views import Create, Enter, Inventory, PriceOzon

urlpatterns = [
    path('create/', Create.as_view(), name='create'),
    path('inventory/', Inventory.as_view(), name='inventory'),
    path('price_ozon/', PriceOzon.as_view(), name='price_ozon'),
    path('', Enter.as_view(), name='enter'),
]
