# Generated by Django 5.1.2 on 2024-10-18 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LITRevu', '0002_delete_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='name',
            field=models.CharField(blank=True, max_length=8192),
        ),
    ]
