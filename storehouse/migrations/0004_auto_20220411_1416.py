# Generated by Django 3.1.4 on 2022-04-11 11:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('storehouse', '0003_auto_20220108_1414'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='storehouses',
            options={'ordering': ['-pk'], 'verbose_name': 'Отделения', 'verbose_name_plural': 'Отделение'},
        ),
        migrations.AlterModelOptions(
            name='storerelated',
            options={'ordering': ['-pk'], 'verbose_name': 'Связанные отделения', 'verbose_name_plural': 'Связанное отделение'},
        ),
    ]