# Generated by Django 4.2.1 on 2023-06-28 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0015_remove_product_supplier_alter_category_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='title',
            new_name='name',
        ),
    ]
