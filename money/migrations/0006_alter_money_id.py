# Generated by Django 4.0.5 on 2022-07-03 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0005_auto_20210509_0245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='money',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
