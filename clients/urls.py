from .views import *
from django.urls import include, path

urlpatterns = [
    path('', ClientsHomeView.as_view(), name='clients_home'),
    #path('select2/', include('django_select2.urls')),
]


