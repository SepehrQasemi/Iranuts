# Generated by Django 4.2.1 on 2023-06-30 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_summaries'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='summaries',
            field=models.TextField(blank=True, max_length=250, null=True),
        ),
    ]