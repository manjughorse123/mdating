# Generated by Django 4.0 on 2022-01-19 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('post', '0004_alter_postupload_likes_alter_postupload_shares_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postreaction',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.user', unique=True),
        ),
    ]
