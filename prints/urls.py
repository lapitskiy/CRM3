from django.urls import path, include
from .views import *

urlpatterns = [
    path('', PrintsHomeView.as_view(), name='prints_home'),
    path('tinymce/', include('tinymce.urls')),
]


