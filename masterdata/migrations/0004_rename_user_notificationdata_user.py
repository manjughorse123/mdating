# Generated by Django 4.0.1 on 2022-12-28 05:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('masterdata', '0003_rename_motification_message_notificationdata_notification_message'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notificationdata',
            old_name='User',
            new_name='user',
        ),
    ]