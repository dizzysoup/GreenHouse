# Generated by Django 3.2.9 on 2021-12-09 12:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('espsensor', '0002_soil'),
    ]

    operations = [
        migrations.CreateModel(
            name='SensorList',
            fields=[
                ('Serial_id', models.AutoField(primary_key=True, serialize=False)),
                ('SoilMoistureSensor', models.FloatField(blank=True, default=0)),
                ('ESPSerial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Esp_Sensor', to='espsensor.esp')),
                ('GH', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='GreenHouse', to='espsensor.greenhouse')),
            ],
            options={
                'db_table': 'SensorList',
            },
        ),
    ]
