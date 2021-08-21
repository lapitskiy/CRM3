from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator
from django.db.models import Q
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Prints(models.Model):
    name = models.CharField(max_length=150, blank=True, verbose_name='Название')
    contentform = RichTextUploadingField()
    related_uuid = models.JSONField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('view_prints', kwargs={'pk': self.pk})

    @property
    def get_related_data(self):
        data = {
            'related_use': 'menu',
            'module_name': 'Печать',
            'link': '../prints/form/?uuid=',
            'form': self.pk
            }
        return data

    def get_related_html(self):
        data = {
            'Печать': 'Button here',
            }
        return data

    def get_related_filter(self, **kwargs):
        pass
        return


    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Форма'
        verbose_name_plural = 'Формы'
        ordering = ['-pk']