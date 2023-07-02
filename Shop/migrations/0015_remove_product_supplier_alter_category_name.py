# Generated by Django 4.2.1 on 2023-06-28 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0014_category_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='supplier',
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]