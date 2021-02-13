from django.db import models
from django.urls import reverse


class Plugins(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    module_name = models.CharField(max_length=150, blank=True, verbose_name='Имя модуля')
    version = models.IntegerField(default=1, verbose_name='Версия')
    description = models.TextField(blank=True, verbose_name='Описание')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name='Фото')
    is_active = models.BooleanField(default=False, verbose_name='Активирован')
    category = models.ForeignKey('PluginsCategory', on_delete=models.PROTECT, verbose_name='Категория', related_name='get_category')
    is_migrate = models.BooleanField(default=False, verbose_name='Миграция')

    def get_absolute_url(self):
        return reverse('urls_view_current_plugins', kwargs={'pk': self.pk})



    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Плагин'
        verbose_name_plural = 'Плагины'
        ordering = ['title']


class PluginsCategory(models.Model):

    title = models.CharField(max_length=150, db_index=True, verbose_name='Наименования категории')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']