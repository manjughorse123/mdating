# Generated by Django 4.0.1 on 2022-02-17 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_user_govt_id_user_is_govt_id_verified_user_selfie'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_register_user_verified',
            field=models.BooleanField(default=False),
        ),
    ]
