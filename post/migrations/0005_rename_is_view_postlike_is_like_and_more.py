# Generated by Django 4.0.1 on 2022-02-28 09:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_rename_is_like_postupload_is_like_count_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postlike',
            old_name='is_view',
            new_name='is_like',
        ),
        migrations.RenameField(
            model_name='postview',
            old_name='is_like',
            new_name='is_view',
        ),
    ]
