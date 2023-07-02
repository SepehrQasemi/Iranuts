# Generated by Django 4.2.1 on 2023-06-22 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0006_city_province_delete_form_city_province'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='slug',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='province',
            name='slug',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
