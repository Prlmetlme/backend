# Generated by Django 4.0.6 on 2022-09-28 01:20

import django.contrib.auth.models
from django.db import migrations, models
import misc_utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(auto_created=True, default=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('birthday', models.DateField(blank=True, null=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to=misc_utils.upload_image)),
                ('banner_image', models.ImageField(blank=True, null=True, upload_to=misc_utils.upload_image)),
                ('date_joined', models.DateField(auto_now_add=True)),
                ('last_active', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(blank=True, max_length=35)),
                ('last_name', models.CharField(blank=True, max_length=35)),
                ('phone', models.CharField(blank=True, max_length=12)),
                ('occupation', models.CharField(blank=True, max_length=30)),
                ('username', models.CharField(max_length=40, unique=True)),
                ('email', models.EmailField(max_length=100)),
                ('bio', models.TextField(blank=True)),
                ('static_user_id', models.CharField(default=misc_utils.id_generator, editable=False, max_length=36, unique=True)),
                ('privated', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
