# Generated by Django 4.0.1 on 2022-02-02 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_user_passion_in'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='passion_in',
            field=models.ManyToManyField(blank=True, null=True, to='account.Passion'),
        ),
    ]