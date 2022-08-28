from .models import Status, Category_service
from django.contrib.auth.models import User

def getActiveStatus(**kwargs):
    queryset = Status.objects.filter(active_creation=True)
    return queryset

def getCategoryServicePermission(**kwargs):
    queryset = Category_service.objects.filter(user_permission=kwargs['user'])
    #queryset = Storehouses.objects.all()
    return queryset