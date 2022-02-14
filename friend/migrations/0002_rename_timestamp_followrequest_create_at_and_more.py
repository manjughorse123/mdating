# Generated by Django 4.0.1 on 2022-02-14 09:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('friend', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='followrequest',
            old_name='timestamp',
            new_name='create_at',
        ),
        migrations.RenameField(
            model_name='friendrequest',
            old_name='timestamp',
            new_name='create_at',
        ),
        migrations.AddField(
            model_name='followaccept',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.date(2022, 2, 14)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='friendlist',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.date(2022, 2, 14)),
            preserve_default=False,
        ),
    ]
