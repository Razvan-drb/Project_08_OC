# Generated by Django 5.1.2 on 2024-11-29 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LITRevu', '0009_critiquefeedback'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='critique',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='critique',
            name='rating',
        ),
    ]
