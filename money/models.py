from django.db import models
from django.urls import reverse
from django.db.models import Q

# Create your models here.
class Money(models.Model):
    money = models.DecimalField(max_digits=19, blank=True, default=0, decimal_places=2, verbose_name='Сумма')
    prepayment = models.DecimalField(max_digits=19, blank=True, default=0, decimal_places=2, verbose_name='Предоплата')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    #related_uuid = models.CharField(max_length=22, blank=True, verbose_name='uuid')
    related_uuid = models.JSONField(blank=True) # json dict

    def get_absolute_url(self):
        return reverse('view_money', kwargs={'pk': self.pk})

    def get_related_data(self):
        data = {
            'related_use': 'data',
            'module_name': 'Стоимость',
            'Сумма': self.money,
            'Предоплата': self.prepayment,
            'related_uuid': self.related_uuid,
            }
        return data

    def get_related_filter(self, **kwargs):
        results = Money.objects.filter(Q(money__icontains=kwargs['search_query']) | Q(prepayment__icontains=kwargs['search_query']))
        return results

    def __str__(self):
        return str(self.money)

    class Meta:
        verbose_name = 'Деньги'
        verbose_name_plural = 'Деньги'
        ordering = ['-created_at']