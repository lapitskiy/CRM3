from django.urls import path

from .views import Create, Store

urlpatterns = [
    path('', Create.as_view(), name='create'),
    path('store', Store.as_view(), name='store'),
]