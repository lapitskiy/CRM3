from django.urls import path
from .views import *

urlpatterns = [
    path('', UsersHomeViewPermit, name='user_home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]