from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator

# Create your models here.
class Clients(models.Model):
    name = models.CharField(max_length=150, verbose_name='Имя')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True, verbose_name='Телефон') # validators should be a list
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    related = models.ForeignKey('Related', null=True, on_delete=models.PROTECT, verbose_name='Связь', related_name='get_related')

    def get_absolute_url(self):
        return reverse('view_clients', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['-created_at']


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