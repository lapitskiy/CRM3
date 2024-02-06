# Generated by Django 5.0.1 on 2024-02-05 19:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0006_phone_remove_clients_related_uuid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clients',
            name='phone',
            field=models.CharField(max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+79998887766'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Телефон'),
        ),
        migrations.DeleteModel(
            name='Phone',
        ),
    ]
