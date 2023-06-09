# Generated by Django 4.0.1 on 2022-10-17 06:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0003_alter_user_govt_id_alter_user_selfie'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_text_read', models.BooleanField(default=False)),
                ('is_text', models.TextField(blank=True, null=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('receiver', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_receiver', to='account.user')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_sender', to='account.user')),
            ],
        ),
    ]
