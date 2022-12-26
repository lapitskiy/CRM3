from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator
from django.db.models import Q
from django.forms.models import model_to_dict

# Create your models here.GHH
class Clients(models.Model):
    name = models.CharField(max_length=150, blank=True, verbose_name='Имя')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+79998887766'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17, verbose_name='Телефон') # validators should be a list
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    #related_uuid = models.CharField(max_length=22, blank=True, verbose_name='uuid')
    related_uuid = models.JSONField(blank=True) # json dict
    uuid = models.ManyToManyField('RelatedUuid')

    def get_absolute_url(self):
        return reverse('view_clients', kwargs={'pk': self.pk})

    def get_related_data(self, **kwargs):
        data = {
            'related_use': 'form',
            'module_name': 'Контакт',
            'Телефон': self.phone,
            'related_uuid': list(self.uuid.values_list('related_uuid', flat=True)),
            }
        return data

    def get_related_dict_data(self):
        return model_to_dict(self)

    def get_related_filter(self, **kwargs):
        results = Clients.objects.filter(Q(phone__icontains=kwargs['search_query']))
        return results

    @classmethod
    def get_related_by_uuid(cls, uuid):
        return Clients.objects.get(uuid__related_uuid=uuid)


    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['-created_at']

class RelatedUuid(models.Model):
    related_uuid = models.CharField(max_length=25, verbose_name='uuid', unique=True)

    class Meta:
        verbose_name = 'uuid'
        verbose_name_plural = 'uuid'
        ordering = ['pk']