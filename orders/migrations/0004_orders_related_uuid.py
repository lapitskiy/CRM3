# Generated by Django 3.1.4 on 2021-03-17 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_remove_orders_related'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='related_uuid',
            field=models.CharField(blank=True, max_length=22, verbose_name='uuid'),
        ),
    ]
