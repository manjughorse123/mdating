# Generated by Django 4.0.1 on 2022-02-01 06:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='first_count',
        ),
    ]
