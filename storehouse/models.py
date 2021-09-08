from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator
from django.db.models import Q
from django.core.exceptions import ValidationError
import phonenumbers
from django.contrib.auth.models import User

def validate_phone_number(value):
    z = phonenumbers.parse(value, None)
    if not phonenumbers.is_valid_number(z):
        raise ValidationError(
            _('%(value) is not a valid phone number'),
            params={'value': value},
        )

# Create your models here.
class Storehouses(models.Model):
    name = models.CharField(max_length=150, blank=True, verbose_name='Название')
    address = models.CharField(max_length=200, blank=True, verbose_name='Название')
    phone = models.CharField(validators=[validate_phone_number], unique=True, max_length=17, verbose_name='Телефон')
    category = models.ForeignKey('Category', default=1, on_delete=models.PROTECT, verbose_name='Категория', related_name='get_category')
    related_user = models.ForeignKey(User, related_name='storehouse_user', null=True, blank=True, on_delete=models.PROTECT, verbose_name='Owner')
    related_uuid = models.JSONField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('view_storehouse', kwargs={'pk': self.pk})

    @property
    def get_related_data(self):
        data = {
            'related_use': 'menu',
            'module_name': 'Склады',
            'link': '../storehouse/form/?uuid=',
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


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименования категории')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']