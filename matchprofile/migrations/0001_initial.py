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
            name='UserToUserUnLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('craeted', models.DateTimeField(auto_now=True)),
                ('like_profile_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_user_profie', to='account.user')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_user_to_unlike', to='account.user')),
            ],
        ),
        migrations.CreateModel(
            name='UserToUserLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_like', models.BooleanField(default=False)),
                ('craeted', models.DateTimeField(auto_now=True)),
                ('like_profile_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like_user', to='account.user')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_to_user', to='account.user')),
            ],
        ),
        migrations.CreateModel(
            name='UserMatchProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_like', models.BooleanField(default=False)),
                ('craeted', models.DateTimeField(auto_now=True)),
                ('like_profile_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_match_user', to='account.user')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_matches', to='account.user')),
            ],
        ),
        migrations.CreateModel(
            name='PostUserUpdate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_view', models.IntegerField(default=0)),
                ('post', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_user', to='account.user')),
            ],
        ),
        migrations.CreateModel(
            name='PostUserReact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_react', to='matchprofile.postuserupdate')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_user_visit', to='account.user')),
            ],
        ),
        migrations.CreateModel(
            name='NewUserMatchProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like_profile_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='new_user_like', to='account.user')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='new_user_match', to='account.user')),
            ],
        ),
    ]
