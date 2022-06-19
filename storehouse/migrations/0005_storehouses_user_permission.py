# Generated by Django 3.1.4 on 2022-04-19 21:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('storehouse', '0004_auto_20220411_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='storehouses',
            name='user_permission',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
