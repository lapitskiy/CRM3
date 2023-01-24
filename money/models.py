from django.db import models
from django.urls import reverse
from django.db.models import Q
from decimal import Decimal
from django.db.models import Sum
from django.forms.models import model_to_dict

# Create your models here.
class Money(models.Model):
    money = models.DecimalField(max_digits=19, default=0, decimal_places=2, verbose_name='Сумма')
    #prepayment = models.DecimalField(max_digits=19, blank=True, default=0, decimal_places=2, verbose_name='Оплачено')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    #updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    updated_dict = models.JSONField(blank=True, default=dict)  # json dict
    #related_uuid = models.CharField(max_length=22, blank=True, verbose_name='uuid')
    related_uuid = models.JSONField(blank=True, null=True) # json dict
    uuid = models.ManyToManyField('RelatedUuid')
    card_pay = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('view_money', kwargs={'pk': self.pk})

    def get_related_data(self, **kwargs):
        prepayment = Prepayment.get_all_prepayment_sum(id=self.pk)
        if prepayment is None:
            prepayment = 0
        pay_method = 'Наличные'
        if self.card_pay == True:
            pay_method = 'По карте'
        data = {
            'related_use': 'form',
            'module_name': 'Стоимость',
            'Сумма': self.money,
            'Оплачено': prepayment,
            'Способ оплаты':  pay_method,
            'html': '<a href="/money/edit/'+str(self.pk)+'" target="_blank">Внести предоплату</a>',
            'related_uuid': list(self.uuid.values_list('related_uuid', flat=True)),
            }

        if self.money != prepayment:
            data['warning'] = 'red'
        return data

    def get_related_dict_data(self):
        dict_ = model_to_dict(self)
        prepayment = Prepayment.get_all_prepayment_sum(id=self.pk)
        if prepayment is None:
            prepayment = 0
        dict_.update({'prepayment': prepayment})
        return dict_

    def get_related_filter(self, **kwargs):
        results = Money.objects.filter(Q(money__icontains=kwargs['search_query']))
        return results

    @classmethod
    def get_related_by_uuid(self, uuid):
        return Money.objects.get(uuid__related_uuid=uuid)

    def __str__(self):
        return str(self.money)

    class Meta:
        verbose_name = 'Деньги'
        verbose_name_plural = 'Деньги'
        ordering = ['-created_at']

# Create your models here.
class Prepayment(models.Model):
    money = models.ForeignKey(Money, related_name='prep_money', on_delete=models.PROTECT, verbose_name='Сумма')
    prepayment = models.DecimalField(max_digits=19, default=0, decimal_places=2, verbose_name='Предоплата')
    comment = models.CharField(max_length=150, blank=True, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Предоплата'
        verbose_name_plural = 'Предоплата'
        ordering = ['-created_at']

    @classmethod
    def get_all_prepayment_sum(cls, id):
        prepay = cls.objects.filter(money=id).aggregate(Sum('prepayment'))['prepayment__sum']
        if prepay is None:
            return Decimal('0.0')
        return cls.objects.filter(money=id).aggregate(Sum('prepayment'))['prepayment__sum']

    def getPrepaySum(self, **kwargs):
        results = Prepayment.objects.filter(pk=self.pk)
        sum_ = Decimal('0.0')
        for x in results:
            sum_ = sum_ + x.prepayment
        return sum_

class RelatedUuid(models.Model):
    related_uuid = models.CharField(max_length=25, verbose_name='uuid', unique=True)

    class Meta:
        verbose_name = 'uuid'
        verbose_name_plural = 'uuid'
        ordering = ['pk']