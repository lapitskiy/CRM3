# Generated by Django 4.0.5 on 2022-08-27 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_alter_category_service_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='active_creation',
            field=models.BooleanField(default=False),
        ),
    ]
