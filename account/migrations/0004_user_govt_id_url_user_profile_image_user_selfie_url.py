# Generated by Django 4.0.1 on 2022-11-04 06:44

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_user_govt_id_alter_user_selfie'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='govt_id_url',
            field=models.ImageField(default=datetime.datetime(2022, 11, 4, 6, 44, 40, 303681, tzinfo=utc), upload_to='govt_id_image/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(default=datetime.datetime(2022, 11, 4, 6, 44, 44, 863856, tzinfo=utc), upload_to='profile_image/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='selfie_url',
            field=models.ImageField(default=datetime.datetime(2022, 11, 4, 6, 44, 49, 999276, tzinfo=utc), upload_to='selfie_image/'),
            preserve_default=False,
        ),
    ]
