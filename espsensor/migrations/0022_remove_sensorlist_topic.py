# Generated by Django 4.0.1 on 2022-03-09 14:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('espsensor', '0021_remove_esp_esp_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sensorlist',
            name='Topic',
        ),
    ]
