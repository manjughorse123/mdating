# Generated by Django 4.0.1 on 2022-02-14 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='postupload',
            name='uploadvedio',
            field=models.TextField(blank=True, null=True),
        ),
    ]