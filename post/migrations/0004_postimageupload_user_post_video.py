# Generated by Django 4.0.1 on 2022-12-20 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_postimageupload'),
    ]

    operations = [
        migrations.AddField(
            model_name='postimageupload',
            name='user_post_video',
            field=models.ImageField(blank=True, null=True, upload_to='user_post_video/'),
        ),
    ]
