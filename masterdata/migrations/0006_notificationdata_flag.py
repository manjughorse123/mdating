# Generated by Django 4.0.1 on 2022-12-29 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterdata', '0005_notificationdata_notify_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificationdata',
            name='flag',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
