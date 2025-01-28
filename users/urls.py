from django.urls import path
from .views import *

urlpatterns = [
    path('', UserHomeView.as_view(), name='user_home'),
    path('register_user/', register, name='register_user'),
    path('register_company/', register_company, name='register_company'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('settings/', UsersSettingsView.as_view(), name='settings'),
]