# Generated by Django 4.0.1 on 2022-12-28 06:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_user_govt_id_url_alter_user_profile_image_and_more'),
        ('masterdata', '0004_rename_user_notificationdata_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificationdata',
            name='notify_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Notify_anotheruser', to='account.user'),
        ),
    ]
