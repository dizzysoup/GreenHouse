# Generated by Django 3.2.9 on 2021-12-12 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('espsensor', '0011_auto_20211212_1838'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sensorlist',
            old_name='HumiSensir',
            new_name='HumiSensor',
        ),
    ]
