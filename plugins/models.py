from django.db import models
from django.urls import reverse


class Plugins(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    id_in_rep = models.IntegerField(default=0, blank=True, verbose_name='Id в репозитории')
    module_name = models.CharField(max_length=150, blank=True, verbose_name='Имя модуля')
    version = models.IntegerField(default=1, verbose_name='Версия')
    description = models.TextField(blank=True, verbose_name='Описание')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name='Фото')
    is_active = models.BooleanField(default=False, verbose_name='Активирован')
    category = models.ForeignKey('PluginsCategory', default=1, on_delete=models.PROTECT, verbose_name='Категория', related_name='get_category')
    is_migrate = models.BooleanField(default=False, verbose_name='Миграция')
    related = models.ManyToManyField('self')
    related_class_name = models.CharField(max_length=150, blank=True, verbose_name='Имя класса для связи')


    def get_absolute_url(self):
        return reverse('view_current_plugins', kwargs={'pk': self.pk, 'tag':'show'})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Plugins, self).save(*args, **kwargs)

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

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_id': self.pk})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']
