from django.urls import path
from .views import *

urlpatterns = [
    path('', ViewPlugins.as_view(), name='view_plugins'),
    path('<int:pk>/<str:tag>', ViewCurrentPlugins.as_view(), name='view_current_plugins'),
    path('repository/', ViewRepositoryPlugins.as_view(), name='view_repository'),
    path('repository/<int:id>/<str:tag>', InstallRepositoryPlugins.as_view(), name='install_repository'),
]