from django.db import models
from django.contrib.auth.models import User

class Parser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    moysklad_api = models.CharField(max_length=1024, verbose_name='API мойсклад')
    yandex_api = models.CharField(max_length=1024, default='', blank=True, null=True, verbose_name='API Яндекс')
    wildberries_api = models.CharField(max_length=1024, default='', blank=True, null=True, verbose_name='API wildberries')
    client_id = models.CharField(max_length=128, default='', blank=True, null=True, verbose_name='Client Id Ozon')
    ozon_api = models.CharField(max_length=1024, default='', blank=True, null=True, verbose_name='API Ozon')
    replenishment = models.BooleanField(default=False, verbose_name='Пополняется ли склад сейчас?')