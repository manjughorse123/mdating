# Generated by Django 4.0.1 on 2022-02-15 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('friend', '0003_rename_is_active_friendrequest_friendrequestsent'),
    ]

    operations = [
        migrations.AddField(
            model_name='friendlist',
            name='is_accepted',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
    ]