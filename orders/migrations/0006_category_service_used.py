# Generated by Django 4.0.5 on 2022-07-11 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_alter_category_service_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category_service',
            name='used',
            field=models.IntegerField(default=0),
        ),
    ]
