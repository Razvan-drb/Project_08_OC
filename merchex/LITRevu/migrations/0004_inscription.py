# Generated by Django 5.1.2 on 2024-10-25 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LITRevu', '0003_ticket_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=128)),
            ],
        ),
    ]
