from .models import Storehouses
from django.contrib.auth.models import User

def getStoresListByUser(**kwargs):
    #print('- request.user: ', kwargs['user'])
    queryset = Storehouses.objects.filter(user_permission=kwargs['user'])
    #queryset = Storehouses.objects.all()
    return queryset