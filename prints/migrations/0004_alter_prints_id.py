# Generated by Django 4.0.5 on 2022-07-03 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prints', '0003_auto_20210723_0251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prints',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
