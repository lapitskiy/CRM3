from django.urls import path
from .views import *

urlpatterns = [
    path('', ViewPlugins.as_view(), name='view_plugins'),
    path('<int:pk>/', ViewCurrentPlugins.as_view(), name='view_current_plugins'),
    path('repository/', ViewRepositoryPlugins.as_view(), name='view_repository'),
    path('repository/<int:id>/', InstallRepositoryPlugins.as_view(), name='install_repository'),
]