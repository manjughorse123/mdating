# Generated by Django 4.0.1 on 2022-12-28 05:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('masterdata', '0002_notificationdata'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notificationdata',
            old_name='motification_message',
            new_name='notification_message',
        ),
    ]
