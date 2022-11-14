# Generated by Django 4.1.1 on 2022-11-07 23:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('catalog_number', models.CharField(max_length=4)),
                ('description', models.CharField(max_length=64)),
                ('units', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('major', models.TextField()),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('friends', models.ManyToManyField(blank=True, related_name='friends', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_number', models.IntegerField(default=0)),
                ('wait_list', models.IntegerField(default=0)),
                ('wait_cap', models.IntegerField(default=0)),
                ('enrollment_total', models.IntegerField(default=0)),
                ('enrollment_available', models.IntegerField(default=0)),
                ('topic', models.CharField(max_length=64)),
                ('prof_name', models.CharField(max_length=200)),
                ('prof_email', models.CharField(max_length=24)),
                ('days', models.CharField(max_length=128)),
                ('start_time', models.CharField(max_length=128)),
                ('end_time', models.CharField(max_length=128)),
                ('facility_description', models.CharField(max_length=128)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.course')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classes', models.ManyToManyField(related_name='schedules', to='home.section')),
                ('profile', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='schedule', to='home.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Relationship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('send', 'send'), ('accepted', 'accepted')], max_length=8)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='home.profile')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='home.profile')),
            ],
        ),
    ]