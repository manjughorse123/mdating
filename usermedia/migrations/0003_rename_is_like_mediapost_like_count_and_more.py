# Generated by Django 4.0.1 on 2022-03-14 10:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usermedia', '0002_remove_mediapost_is_media'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mediapost',
            old_name='is_like',
            new_name='like_count',
        ),
        migrations.RenameField(
            model_name='mediapost',
            old_name='is_share',
            new_name='share_count',
        ),
        migrations.RenameField(
            model_name='mediapost',
            old_name='is_view',
            new_name='view_count',
        ),
    ]