# Generated by Django 3.1.4 on 2021-02-14 18:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plugins', '0004_auto_20210214_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plugins',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='get_category', to='plugins.pluginscategory', verbose_name='Категория'),
        ),
    ]