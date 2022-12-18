from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator
from django.db.models import Q
from django.core.exceptions import ValidationError
import phonenumbers
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.forms.models import model_to_dict

def validate_phone_number(value):
    try:
        z = phonenumbers.parse(value, None)
    except phonenumbers.NumberParseException:
        print('NOT VALID 0')
        raise ValidationError(
            _('%s is not a valid phone number'),
            params=value,)
    if not phonenumbers.is_valid_number(z):
        print('NOT VALID')
        raise ValidationError(
            _('%(value) is not a valid phone number'),
            params={'value': value},
        )


# Create your models here.
class StoreRelated(models.Model):
    store = models.ForeignKey('Storehouses', null=True, on_delete=models.PROTECT, verbose_name='Отделение', related_name='get_storehouse', blank=False)
    related_uuid = models.JSONField(blank=True, null=True)
    uuid = models.ManyToManyField('RelatedUuid')

    def get_related_data(self, **kwargs):
        data = {
            'related_use': 'text',
            'module_name': 'Отделения',
            'related_text': 'Отделение '+self.store.name,
            'related_uuid': list(self.uuid.values_list('related_uuid', flat=True)),
            }
        return data

    def get_related_filter(self, **kwargs):
        pass
        return

    def get_related_dict_data(self):
        return model_to_dict(self)

    @classmethod
    def get_related_uuid(cls, uuid):
        return StoreRelated.objects.get(pk=RelatedUuid.objects.get(related_uuid=uuid).related)

    def __str__(self):
        return str(self.store.name)

    class Meta:
        verbose_name = 'Связанные отделения'
        verbose_name_plural = 'Связанное отделение'
        ordering = ['-pk']

# Create your models here.
class Storehouses(models.Model):
    name = models.CharField(max_length=150, blank=True, verbose_name='Название')
    address = models.CharField(max_length=200, blank=True, verbose_name='Адрес')
    phone = models.CharField(validators=[validate_phone_number], unique=True, max_length=17, verbose_name='Телефон')
    category = models.ForeignKey('Category', default=1, on_delete=models.PROTECT, verbose_name='Категория', related_name='get_category')
    user_permission = models.ManyToManyField(User)
    related_user = models.ForeignKey(User, related_name='storehouse_user', null=True, blank=True, on_delete=models.PROTECT, verbose_name='Owner')



    def get_absolute_url(self):
        return reverse('view_storehouse', kwargs={'pk': self.pk})


    def get_related_filter(self, **kwargs):
        pass
        return


    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Отделения'
        verbose_name_plural = 'Отделение'
        ordering = ['-pk']


class Category(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name='Наименования категории')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']

class RelatedUuid(models.Model):
    related_uuid = models.CharField(max_length=25, verbose_name='uuid', unique=True)

    class Meta:
        verbose_name = 'uuid'
        verbose_name_plural = 'uuid'
        ordering = ['pk']