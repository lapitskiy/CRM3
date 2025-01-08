from django.db import models
from django.contrib.auth.models import User

# python manage.py makemigrations
# python manage.py migrate

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    moysklad_api = models.CharField(max_length=512, unique=True, verbose_name='API мойсклад')
    yandex_api = models.CharField(max_length=512, unique=True, verbose_name='API Яндекс')
    wildberries_api = models.CharField(max_length=512, unique=True, verbose_name='API wildberries')
    client_id = models.CharField(max_length=512, unique=True, verbose_name='Client Id Ozon')
    ozon_api = models.CharField(max_length=512, unique=True, verbose_name='API Ozon')
    stock_update_at = models.DateTimeField(blank=True, null=True, verbose_name='Последняя инвентаризация')

class Crontab(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, verbose_name='Связанный парсер')
    name = models.CharField(max_length=150, null=True, blank=True)
    yandex = models.BooleanField(default=False, verbose_name='yandex')
    ozon = models.BooleanField(default=False, verbose_name='ozon')
    wb = models.BooleanField(default=False, verbose_name='wb')
    crontab_dict = models.JSONField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['seller', 'name'], name='unique_crontab')
        ]

class Awaiting(models.Model):
    '''
    status:
    awaiting_deliver - ожидает отгрузки
    '''
    posting_number = models.CharField(max_length=30, null=False, unique=True)
    status = models.CharField(max_length=30, null=False)
    market = models.CharField(max_length=30, null=False) #ozon, wb, yandex


class Awaiting_product(models.Model):
    awaiting = models.ForeignKey(Awaiting, on_delete=models.CASCADE, verbose_name='Связанный заказ')
    offer_id = models.CharField(max_length=50, null=False)
    price = models.IntegerField(null=False, verbose_name='Цена')
    quantity = models.IntegerField(null=False, verbose_name='Количество')

class Metadata(models.Model):
    '''
    name:
    ms_storage_ozon - склад для озон
    ms_storage_wb - склад для wb
    ms_storage_yandex - склад для yandex
    ms_organization - юр.лицо или название компании
    ms_ozon_contragent - метадата данные контрагент озон
    ms_yandex_contragent - метадата данные контрагент яндекс
    ms_wb_contragent - метадата данные контрагент wb
    ms_status_awaiting - мета статус заказа покупателя
    ms_status_shipped - мета статус заказа покупателя
    ms_status_completed - мета статус заказа покупателя
    ms_status_cancelled - мета статус заказа покупателя
    '''
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, verbose_name='Связанный парсер')
    name = models.CharField(max_length=50, null=False)
    metadata_dict = models.JSONField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['seller', 'name'], name='unique_metadata')
        ]


