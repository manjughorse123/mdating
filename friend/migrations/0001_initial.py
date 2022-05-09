# Generated by Django 4.0.1 on 2022-04-11 11:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255)),
                ('answer', models.TextField(blank=True, null=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='FriendRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friendrequestsent', models.BooleanField(default=False)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='account.user')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend', to='account.user')),
            ],
        ),
        migrations.CreateModel(
            name='FriendList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_accepted', models.BooleanField(default=False)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('friends', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='friends', to='account.user')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='account.user')),
            ],
        ),
        migrations.CreateModel(
            name='FollowRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_follow', models.BooleanField(default=False)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('follow', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='Follow_user', to='account.user')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent_user', to='account.user')),
            ],
        ),
        migrations.CreateModel(
            name='FollowAccept',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_follow_accepted', models.BooleanField(default=False)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('follow', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='Follow_user_accept', to='account.user')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent_user_accept', to='account.user')),
            ],
        ),
    ]
