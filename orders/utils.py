from .models import Status
from django.contrib.auth.models import User

def getActiveStatus(**kwargs):
    queryset = Status.objects.filter(active_creation=True)
    return queryset