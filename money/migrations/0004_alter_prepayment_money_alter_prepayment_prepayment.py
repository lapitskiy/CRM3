# Generated by Django 4.1.1 on 2022-11-15 22:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0003_alter_money_updated_dict'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prepayment',
            name='money',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='prep_money', to='money.money', verbose_name='Сумма'),
        ),
        migrations.AlterField(
            model_name='prepayment',
            name='prepayment',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=19, verbose_name='Предоплата'),
        ),
    ]