from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

class Device(models.Model):
    name = models.CharField(max_length=150, db_index=True, unique=True)
    used = models.IntegerField(default=0)
    category_service = models.ForeignKey('Category_service', default=1, on_delete=models.SET_DEFAULT, null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Устройство'
        verbose_name_plural = 'Устройство'
        ordering = ['name']

# Create your models here.
class Orders(models.Model):
    serial = models.CharField(max_length=150, blank=True, verbose_name='Серийный')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name='Обновлен')
    status = models.ForeignKey('Status', default=1, on_delete = models.SET_DEFAULT, null=True, verbose_name='Статус', related_name='get_status')
    service = models.ForeignKey('Service', default=1, on_delete = models.SET_DEFAULT, null=True, verbose_name='Услуга', related_name='get_service')
    device = models.ForeignKey(Device, default=1,  on_delete = models.SET_DEFAULT, null=True, verbose_name='Устройство', related_name='get_device')
    category = models.ForeignKey('Category', default=1, on_delete = models.SET_DEFAULT, null=True, verbose_name='Категория приемки', related_name='get_category') # fast or simple
    category_service = models.ForeignKey('Category_service', default=1, on_delete=models.SET_DEFAULT, null=True, verbose_name='Категория услуги', related_name='get_category_service')
    related_uuid = models.JSONField(blank=True, null=True) # json dict
    uuid = models.ManyToManyField('RelatedUuid')
    related_user = models.ForeignKey(User, related_name='order_user', null=True, blank=True, on_delete=models.PROTECT, verbose_name='Owner')



    def get_absolute_url(self):
        return reverse('view_orders', kwargs={'pk': self.pk})

    @classmethod
    def get_related_by_uuid(self, uuid):
        try:
            return Orders.objects.get(uuid__related_uuid=uuid)
        except ObjectDoesNotExist:
            pass


    def get_related_data(self, **kwargs):
        data = {}
        if 'link' in kwargs:
            data['link'] = {
                'related_use': 'link',
                'html': '<a href="/orders/one/' + self.pk + '" target="_blank">Заказ ' + self.pk + '</a>',
                'pk': self.pk,
                'related_uuid': list(self.uuid.values_list('related_uuid', flat=True)),
            }
        if 'value_dict' in kwargs:
            data['value'] = {
                'related_use': 'value',
                'module_name': 'Orders',
                'Серийный': self.serial,
                'Комментарий': self.comment,
                'Создан': self.created_at,
                'Статус': self.status,
                'Услуга': self.service,
                'Устройство': self.device,
                'Категория приемки': self.category,
                'Категория услуги': self.category_service,
                'related_uuid': list(self.uuid.values_list('related_uuid', flat=True)),
                }
        return data

    def get_related_dict_data(self):
        return model_to_dict(self)

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']


class Status(models.Model):
    title = models.CharField(max_length=150, db_index=True, unique=True, verbose_name='Наименования статуса')
    active_creation = models.BooleanField(default=False)
    closed_status = models.BooleanField(default=False)
    fast_closed = models.BooleanField(default=False)
    color = models.CharField(max_length=7, default='#ffc700')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('status', kwargs={'status_id': self.pk})

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'
        ordering = ['title']

# fast - быстрый заказ simple обычный
class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименования категории')
    category = models.CharField(max_length=150, db_index=True, unique=True, verbose_name='Категория')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']

class Category_service(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Наименования категории услуги')
    #category = models.CharField(max_length=150, db_index=True,  verbose_name='Категория')
    used = models.IntegerField(default=0)
    user_permission = models.ManyToManyField(User)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категории услуги'
        verbose_name_plural = 'Категории услуги'
        ordering = ['name']

class Service(models.Model):
    name = models.CharField(max_length=150, db_index=True, unique=True, verbose_name='Наименования услуги')
    used = models.IntegerField(default=0)
    category_service = models.ForeignKey('Category_service', default=1, on_delete=models.SET_DEFAULT, null=True)

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ['name']


class RelatedUuid(models.Model):
    related_uuid = models.CharField(max_length=25, verbose_name='uuid', unique=True)

    class Meta:
        verbose_name = 'uuid'
        verbose_name_plural = 'uuid'
        ordering = ['pk']