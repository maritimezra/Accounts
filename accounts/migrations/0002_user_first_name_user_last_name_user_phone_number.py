# Generated by Django 5.0.2 on 2024-02-12 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, default=None, max_length=15, null=True, unique=True),
        ),
    ]
