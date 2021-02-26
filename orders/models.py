from django.db import models
from django.urls import reverse

# Create your models here.
class Orders(models.Model):

    # 44 урок добавиьт фильтр для вывода конкретных статусов и категорий в заказах
    # посомтреть след уроки, надо поставить возможность регистрации мастеров
    # после сделать плагин аккаунты и связать плагины заказы и аккаунты
    # сделать ajax для django orders


    device = models.CharField(max_length=150, verbose_name='Что ремонтируем')
    serial = models.CharField(max_length=150, blank=True, verbose_name='Серийный')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    status = models.ForeignKey('Status', null=True, blank=True, on_delete=models.PROTECT, verbose_name='Статус', related_name='get_status')
    service = models.ForeignKey('Service', null=True, blank=True, on_delete=models.PROTECT, verbose_name='Услуга', related_name='get_service')
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.PROTECT, verbose_name='Категория', related_name='get_category')
    related = models.ForeignKey('Related', null=True, on_delete=models.PROTECT, verbose_name='Связь', related_name='get_related')

    def get_absolute_url(self):
        return reverse('view_orders', kwargs={'pk': self.pk})

    def __str__(self):
        return self.device

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']


class Status(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='Наименования статуса')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('status', kwargs={'status_id': self.pk})

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'
        ordering = ['title']

class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='Наименования категории')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']

class Service(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='Наименования категории')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']

class Related(models.Model):
    plugin = models.CharField(max_length=150, db_index=True, verbose_name='Наименования плагина')
    related_id = models.IntegerField(default=0)

    def __str__(self):
        return self.plugin

    def get_absolute_url(self):
        return reverse('related', kwargs={'related_id': self.pk})

    class Meta:
        verbose_name = 'Связанные'
        verbose_name_plural = 'Связанные данные'
        ordering = ['plugin']