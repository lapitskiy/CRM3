# Generated by Django 3.1.4 on 2021-03-17 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plugins', '0010_auto_20210304_2244'),
    ]

    operations = [
        migrations.AddField(
            model_name='plugins',
            name='related_class_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='Имя класса для связи'),
        ),
    ]
