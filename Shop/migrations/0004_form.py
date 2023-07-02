# Generated by Django 4.2.1 on 2023-05-22 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0003_rename_titles_product_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('phone', models.IntegerField(max_length=13)),
                ('email', models.EmailField(max_length=254)),
                ('skils', models.TextField()),
            ],
        ),
    ]
