# Generated by Django 4.0.1 on 2022-02-01 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_gender_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idealmatch',
            name='icon',
            field=models.ImageField(default=1, upload_to='idealMatch_icon/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='maritalstatus',
            name='icon',
            field=models.ImageField(default=1, upload_to='maritalstatus_icon/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='passion',
            name='icon',
            field=models.ImageField(default=1, upload_to='passion_icon/'),
            preserve_default=False,
        ),
    ]
