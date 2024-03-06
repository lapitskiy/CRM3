from django.urls import path

from .views import Create, Enter, Inventory

urlpatterns = [
    path('create/', Create.as_view(), name='create'),
    path('inventory/', Inventory.as_view(), name='inventory'),
    path('', Enter.as_view(), name='enter'),
]