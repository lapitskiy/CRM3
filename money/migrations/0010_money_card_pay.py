# Generated by Django 4.1.1 on 2023-01-23 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0009_alter_money_related_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='money',
            name='card_pay',
            field=models.BooleanField(default=False),
        ),
    ]
