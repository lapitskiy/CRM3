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
    related_uuid = models.CharField(max_length=22, blank=True, verbose_name='uuid')

    def get_absolute_url(self):
        return reverse('view_clients', kwargs={'pk': self.pk})

    def get_related_data(self):
        data = {
            'module_name': 'Контакт',
            'Имя': self.name,
            'Телефон': self.phone,
            'related_uuid': self.related_uuid,
            }
        return data

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['-created_at']