# Generated by Django 4.1.1 on 2022-11-07 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='calendar',
            name='date',
        ),
        migrations.AddField(
            model_name='calendar',
            name='mock',
            field=models.CharField(max_length=4, null=True),
        ),
    ]