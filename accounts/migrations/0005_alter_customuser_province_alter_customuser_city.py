# Generated by Django 4.2.1 on 2023-06-30 07:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0018_alter_supplier_phone'),
        ('accounts', '0004_alter_customuser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='Province',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Shop.province'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Shop.city'),
        ),
    ]