# Generated by Django 4.1.1 on 2022-11-10 23:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_alter_course_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.department'),
        ),
    ]
