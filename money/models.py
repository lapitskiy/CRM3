from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator

# Create your models here.
class Money(models.Model):
    money = models.DecimalField(max_digits=19, blank=True, default=0, decimal_places=4)
    prepayment = models.DecimalField(max_digits=19, blank=True, default=0, decimal_places=4)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    related_uuid = models.CharField(max_length=22, blank=True, verbose_name='uuid')

    def get_absolute_url(self):
        return reverse('view_money', kwargs={'pk': self.pk})

    def get_related_data(self):
        data = {
            'module_name': 'Стоимость',
            'Сумма': self.money,
            'Предоплата': self.prepayment,
            'related_uuid': self.related_uuid,
            }
        return data

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Деньги'
        verbose_name_plural = 'Деньги'
        ordering = ['-created_at']