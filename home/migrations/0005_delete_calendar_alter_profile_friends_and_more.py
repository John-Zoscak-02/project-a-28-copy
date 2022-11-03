# Generated by Django 4.1.1 on 2022-10-31 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Calendar',
        ),
        migrations.AlterField(
            model_name='profile',
            name='friends',
            field=models.ManyToManyField(blank=True, null=True, to='home.profile'),
        ),
        migrations.AlterField(
            model_name='section',
            name='schedules',
            field=models.ManyToManyField(null=True, related_name='classes', to='home.profile'),
        ),
        migrations.DeleteModel(
            name='Schedule',
        ),
    ]
