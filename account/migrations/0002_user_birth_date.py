# Generated by Django 4.0 on 2021-12-31 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='birth_date',
            field=models.DateField(blank=True, default='1999-12-15', null=True),
        ),
    ]
