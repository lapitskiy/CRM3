# Generated by Django 4.1.1 on 2022-12-13 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0004_alter_relateduuid_options_remove_relateduuid_related_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relateduuid',
            name='related_uuid',
            field=models.CharField(max_length=25, unique=True, verbose_name='uuid'),
        ),
    ]
