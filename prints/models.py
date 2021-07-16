from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator
from django.db.models import Q
from tinymce.models import HTMLField

# Create your models here.
class Prints(models.Model):
    name = models.CharField(max_length=150, blank=True, verbose_name='Nazvanie')
    contentform = HTMLField()
    related_uuid = models.JSONField(blank=True)

    def get_absolute_url(self):
        return reverse('view_prints', kwargs={'pk': self.pk})

    def get_related_data(self):
        data = {
            'module_name': 'Prints',
            'Имя': self.name,
            'content': self.contentform,
            'related_uuid': self.related_uuid,
            }
        return data

    def get_related_filter(self, **kwargs):
        pass
        return


    def __str__(self):
        return self.pk

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['-pk']