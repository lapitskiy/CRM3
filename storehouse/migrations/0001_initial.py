# Generated by Django 4.0.5 on 2022-09-14 01:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import storehouse.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, unique=True, verbose_name='Наименования категории')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Storehouses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=150, verbose_name='Название')),
                ('address', models.CharField(blank=True, max_length=200, verbose_name='Адрес')),
                ('phone', models.CharField(max_length=17, unique=True, validators=[storehouse.models.validate_phone_number], verbose_name='Телефон')),
                ('category', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='get_category', to='storehouse.category', verbose_name='Категория')),
                ('related_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='storehouse_user', to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
                ('user_permission', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Отделения',
                'verbose_name_plural': 'Отделение',
                'ordering': ['-pk'],
            },
        ),
        migrations.CreateModel(
            name='StoreRelated',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('related_uuid', models.JSONField(blank=True, null=True)),
                ('store', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='get_storehouse', to='storehouse.storehouses', verbose_name='Отделение')),
            ],
            options={
                'verbose_name': 'Связанные отделения',
                'verbose_name_plural': 'Связанное отделение',
                'ordering': ['-pk'],
            },
        ),
    ]
