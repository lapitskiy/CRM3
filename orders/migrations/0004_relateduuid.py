# Generated by Django 4.1.1 on 2022-12-08 19:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_remove_category_service_category_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelatedUuid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('related_uuid', models.CharField(max_length=25, verbose_name='uuid')),
                ('related', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.orders')),
            ],
            options={
                'verbose_name': 'uuid',
                'verbose_name_plural': 'uuid',
                'ordering': ['related'],
            },
        ),
    ]