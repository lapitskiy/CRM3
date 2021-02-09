from django.db import models
from django.urls import reverse

# Create your models here.
class Orders(models.Model):
    gadget = models.CharField(max_length=150, verbose_name='Что ремонтируем')
    serial = models.TextField(blank=True, verbose_name='Серийный')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    status = models.ForeignKey('Status', on_delete=models.PROTECT, verbose_name='Статус', related_name='get_status')

    def get_absolute_url(self):
        return reverse('view_orders', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

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