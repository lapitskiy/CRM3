# Generated by Django 3.1.4 on 2021-07-21 22:43

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prints', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prints',
            name='contentform',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]