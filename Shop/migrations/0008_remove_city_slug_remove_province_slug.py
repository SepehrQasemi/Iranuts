# Generated by Django 4.2.1 on 2023-06-22 16:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0007_city_slug_province_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='province',
            name='slug',
        ),
    ]
