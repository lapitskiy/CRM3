# Generated by Django 3.1.4 on 2021-02-06 22:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=150, verbose_name='Наименования категории')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Plugins',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название')),
                ('module_name', models.CharField(blank=True, max_length=150, verbose_name='Имя модуля')),
                ('version', models.CharField(max_length=150, verbose_name='Версия')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
                ('photo', models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/', verbose_name='Фото')),
                ('path', models.FileField(blank=True, upload_to='file/', verbose_name='Файл')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активирован')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='get_category', to='plugins.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Плагин',
                'verbose_name_plural': 'Плагины',
                'ordering': ['title'],
            },
        ),
    ]
