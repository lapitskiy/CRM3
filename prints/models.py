from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator
from django.db.models import Q
from ckeditor_uploader.fields import RichTextUploadingField
from django.forms.models import model_to_dict

# Create your models here.
class Prints(models.Model):
    name = models.CharField(max_length=150, blank=True, verbose_name='Название')
    contentform = RichTextUploadingField()
    related_uuid = models.JSONField(blank=True, null=True)
    uuid = models.ManyToManyField('RelatedUuid')

    def get_absolute_url(self):
        return reverse('view_prints', kwargs={'pk': self.pk})


    def get_related_data(self, **kwargs):
        data = {}
        if 'related_uuid' in kwargs:
            data = {
                'title': 'Печать',
                '#': '<a href="/prints/form/?uuid='+kwargs['related_uuid']+'" target="_blank">Распечатать</a>',
                }
        return data

    def get_related_dict_data(self):
        return model_to_dict(self)

    def get_related_filter(self, **kwargs):
        pass

    @classmethod
    def get_related_by_uuid(cls, uuid):
        return Prints.objects.get(uuid__related_uuid=uuid)


    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Форма'
        verbose_name_plural = 'Формы'
        ordering = ['-pk']

class RelatedUuid(models.Model):
    related_uuid = models.CharField(max_length=25, verbose_name='uuid', unique=True)

    class Meta:
        verbose_name = 'uuid'
        verbose_name_plural = 'uuid'
        ordering = ['pk']