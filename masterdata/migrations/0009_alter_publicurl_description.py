# Generated by Django 4.0.1 on 2023-01-12 09:51

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('masterdata', '0008_publicurl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicurl',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
