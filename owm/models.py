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
    parser = models.ForeignKey(Parser, on_delete=models.CASCADE, verbose_name='Связанный парсер')
    active = models.BooleanField(default=False, verbose_name='Синхрон включен')
    name = models.CharField(max_length=150, null=True, blank=True)
    yandex = models.BooleanField(default=False, verbose_name='yandex')
    ozon = models.BooleanField(default=False, verbose_name='ozon')
    wb = models.BooleanField(default=False, verbose_name='wb')
    crontab_dict = models.JSONField(null=True, blank=True)


from sqlalchemy import Table, Column, Integer, String, Boolean, JSON, ForeignKey, DateTime, MetaData

metadata = MetaData()

parser_table = Table(
    'owm_parser', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('auth_user.id'), nullable=True),
    Column('moysklad_api', String(512), unique=True),
    Column('yandex_api', String(512), unique=True),
    Column('wildberries_api', String(512), unique=True),
    Column('client_id', String(512), unique=True),
    Column('ozon_api', String(512), unique=True),
    Column('stock_update_at', DateTime, nullable=True),
)

crontab_table = Table(
    'owm_crontab', metadata,
    Column('id', Integer, primary_key=True),
    Column('parser_id', Integer, ForeignKey('owm_parser.id')),
    Column('active', Boolean, default=False),
    Column('name', String(150), nullable=True),
    Column('yandex', Boolean, default=False),
    Column('ozon', Boolean, default=False),
    Column('wb', Boolean, default=False),
    Column('crontab_dict', JSON, nullable=True),
)
