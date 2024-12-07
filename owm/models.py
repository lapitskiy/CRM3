from django.db import models
from django.contrib.auth.models import User

# python manage.py makemigrations
# python manage.py migrate

class Parser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    moysklad_api = models.CharField(max_length=512, unique=True, verbose_name='API мойсклад')
    yandex_api = models.CharField(max_length=512, unique=True, verbose_name='API Яндекс')
    wildberries_api = models.CharField(max_length=512, unique=True, verbose_name='API wildberries')
    client_id = models.CharField(max_length=512, unique=True, verbose_name='Client Id Ozon')
    ozon_api = models.CharField(max_length=512, unique=True, verbose_name='API Ozon')
    stock_update_at = models.DateTimeField(blank=True, null=True, verbose_name='Последняя инвентаризация')

class Crontab(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    active = models.BooleanField(default=False, verbose_name='Синхрон включен')
    name = models.CharField(max_length=150, null=True, blank=True)
    yandex = models.BooleanField(default=False, verbose_name='yandex')
    ozon = models.BooleanField(default=False, verbose_name='ozon')
    wb = models.BooleanField(default=False, verbose_name='wb')
    crontab_dict = models.JSONField(null=True, blank=True)

