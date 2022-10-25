# Generated by Django 4.1.1 on 2022-10-23 20:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_profile_email_profile_major_profile_year'),
    ]

    operations = [
        migrations.CreateModel(
            name='Followers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('year', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'First Year'), (2, 'Second Year'), (3, 'Thrid Year'), (4, 'Fourth Year'), (5, 'Graduate Student'), (6, 'Other')], null=True)),
                ('major', models.CharField(blank=True, max_length=50)),
                ('email', models.EmailField(blank=True, max_length=254)),
            ],
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
        migrations.AddField(
            model_name='followers',
            name='another_user',
            field=models.ManyToManyField(related_name='another_user', to='home.user'),
        ),
        migrations.AddField(
            model_name='followers',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home.user'),
        ),
    ]
