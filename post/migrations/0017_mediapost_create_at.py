# Generated by Django 4.0 on 2022-01-20 06:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0016_mediapost_is_like_mediapost_is_share_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediapost',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
