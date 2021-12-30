# Generated by Django 4.0 on 2021-12-30 10:10

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import main.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BodyType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body_type', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=5000)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('educations', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=5000)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=500)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='IsVerified',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_verified', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=5000)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='RelationshipStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relationship_status', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=5000)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserIdeaMatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ideamatch', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=500)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserInterest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interest', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=500)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media', models.FileField(blank=True, default=None, null=True, upload_to=main.models.upload_image_path_profile)),
                ('mediades', models.CharField(default='this is images', max_length=100)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', ckeditor.fields.RichTextField()),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('birth_date', models.DateField(blank=True, default='1999-12-15', null=True)),
                ('height', models.DecimalField(decimal_places=2, default=180.34, max_digits=10)),
                ('location', models.CharField(default='', max_length=100)),
                ('citylat', models.DecimalField(decimal_places=6, default='-2.0180319', max_digits=9)),
                ('citylong', models.DecimalField(decimal_places=6, default='52.5525525', max_digits=9)),
                ('image', models.ImageField(blank=True, default=None, null=True, upload_to='profile/')),
                ('address', models.CharField(blank=True, max_length=900, null=True)),
                ('city', models.CharField(blank=True, max_length=30, null=True)),
                ('is_premium', models.BooleanField(default=False)),
                ('first_count', models.IntegerField(default=0, help_text='It is 0, if the user is totally new and 1 if the user has saved his standard once')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('body_type', models.ManyToManyField(to='main.BodyType')),
                ('education', models.ManyToManyField(to='main.Education')),
                ('gender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.gender')),
                ('ideamatch', models.ManyToManyField(to='main.UserIdeaMatch')),
                ('is_verified', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.isverified')),
                ('relationship_status', models.ManyToManyField(to='main.RelationshipStatus')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.userprofile')),
                ('userinterest', models.ManyToManyField(to='main.UserInterest')),
                ('usermedia', models.ManyToManyField(to='main.UserMedia')),
            ],
        ),
    ]
