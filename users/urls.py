from django.urls import path
from .views import *

urlpatterns = [
    path('', UserHomeView.as_view(), name='user_home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('settings/', UsersSettingsView.as_view(), name='settings'),
]