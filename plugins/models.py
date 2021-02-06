from django.db import models
from django.urls import reverse

# Create your models here.
class PluginsCrm3(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    imp_name = models.CharField(max_length=150, verbose_name='Системное название')
    path = models.FileField(upload_to='plugins/plugins/', blank=True, verbose_name='Файл')
    version = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('view_plugins', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Плагин'
        verbose_name_plural = 'Плагины'
        ordering = ['title']