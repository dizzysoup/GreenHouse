# Generated by Django 3.2.9 on 2021-12-14 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('espsensor', '0012_rename_humisensir_sensorlist_humisensor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensorlist',
            name='SoilMoistureSensor1',
            field=models.FloatField(blank=True, choices=[('1', 'Active'), ('-1', 'Disable')], default=1),
        ),
    ]
