# Generated by Django 4.0.1 on 2022-02-28 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_alter_postupload_post'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postupload',
            old_name='is_like',
            new_name='is_like_count',
        ),
        migrations.RenameField(
            model_name='postupload',
            old_name='is_share',
            new_name='is_share_count',
        ),
        migrations.RenameField(
            model_name='postupload',
            old_name='is_view',
            new_name='is_view_count',
        ),
        migrations.RenameField(
            model_name='postupload',
            old_name='uploadvedio',
            new_name='uploadvideo',
        ),
        migrations.AddField(
            model_name='postlike',
            name='is_view',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='postshare',
            name='is_share',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='postview',
            name='is_like',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]