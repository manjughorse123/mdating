# Generated by Django 4.0.1 on 2022-04-28 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_postupload_post_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='postupload',
            name='is_private',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
