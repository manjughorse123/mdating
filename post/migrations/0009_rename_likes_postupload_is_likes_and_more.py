# Generated by Django 4.0 on 2022-01-19 14:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0008_alter_postreaction_post_alter_postreaction_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postupload',
            old_name='likes',
            new_name='is_likes',
        ),
        migrations.RenameField(
            model_name='postupload',
            old_name='shares',
            new_name='is_shares',
        ),
        migrations.RenameField(
            model_name='postupload',
            old_name='views',
            new_name='is_views',
        ),
    ]
