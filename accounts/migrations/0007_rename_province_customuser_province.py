# Generated by Django 4.2.2 on 2023-07-02 17:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_customuser_managers_alter_customuser_phone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='Province',
            new_name='province',
        ),
    ]
