# Generated by Django 4.0 on 2022-01-19 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('post', '0007_remove_postreaction_is_like_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postreaction',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Reaction', to='post.postupload'),
        ),
        migrations.AlterField(
            model_name='postreaction',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Reaction', to='account.user'),
        ),
    ]
