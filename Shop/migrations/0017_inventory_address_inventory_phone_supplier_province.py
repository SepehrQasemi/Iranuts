# Generated by Django 4.2.1 on 2023-06-29 14:18

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0016_rename_title_product_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='inventory',
            name='phone',
            field=models.CharField(blank=True, max_length=13, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be in the format: '0999999999'. Up to 11 digits allowed.", regex='^\\+?1?\\d{11,11}$')]),
        ),
        migrations.AddField(
            model_name='supplier',
            name='Province',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='Shop.province'),
            preserve_default=False,
        ),
    ]
