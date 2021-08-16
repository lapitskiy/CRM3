from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Orders(models.Model):
    serial = models.CharField(max_length=150, blank=True, verbose_name='Серийный')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    status = models.ForeignKey('Status', default=1, on_delete=models.PROTECT, verbose_name='Статус', related_name='get_status')
    service = models.ForeignKey('Service', default=1, on_delete=models.PROTECT, verbose_name='Услуга', related_name='get_service')
    device = models.ForeignKey('Device', default=1, on_delete=models.PROTECT, verbose_name='Устройство', related_name='get_device')
    category = models.ForeignKey('Category', default=1, on_delete=models.PROTECT, verbose_name='Категория', related_name='get_category')
    related_uuid = models.JSONField(blank=True) # json dict
    related_user = models.ForeignKey(User, related_name='order_user', null=True, blank=True, on_delete=models.PROTECT, verbose_name='Owner')


    def get_absolute_url(self):
        return reverse('view_orders', kwargs={'pk': self.pk})

    def get_related_data(self):
        data = {
            'related_use': 'data',
            'module_name': 'Orders',
            'Серийный': self.serial,
            'Комментарий': self.comment,
            'Создан': self.created_at,
            'Статус': self.status,
            'Услуга': self.service,
            'Устройство': self.device,
            'Категория': self.category,
            'related_uuid': self.related_uuid,
            }
        return data

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']


class Status(models.Model):
    title = models.CharField(max_length=150, db_index=True, unique=True, verbose_name='Наименования статуса')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('status', kwargs={'status_id': self.pk})

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'
        ordering = ['title']

class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименования категории')
    category = models.CharField(max_length=150, db_index=True, unique=True, verbose_name='Категория')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']

class Service(models.Model):
    name = models.CharField(max_length=150, db_index=True, unique=True, verbose_name='Наименования услуги')
    used = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ['name']

class Device(models.Model):
    name = models.CharField(max_length=150, db_index=True, unique=True, verbose_name='Устройство')
    used = models.IntegerField(default=0)

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'Устройство'
        verbose_name_plural = 'Устройство'
        ordering = ['name']