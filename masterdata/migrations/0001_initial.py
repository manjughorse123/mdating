# Generated by Django 4.0.1 on 2022-12-19 10:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0005_alter_user_govt_id_url_alter_user_profile_image_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CusztomFCMDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Name')),
                ('active', models.BooleanField(default=True, help_text='Inactive devices will not be sent notifications', verbose_name='Is active')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Creation date')),
                ('device_id', models.CharField(blank=True, db_index=True, help_text='Unique device identifier', max_length=255, null=True, verbose_name='Device ID')),
                ('registration_id', models.TextField(verbose_name='Registration token')),
                ('type', models.CharField(choices=[('ios', 'ios'), ('android', 'android'), ('web', 'web')], max_length=10)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fcm_user_id', to='account.user')),
            ],
            options={
                'verbose_name': 'FCM device',
                'abstract': False,
            },
        ),
    ]
