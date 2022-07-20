# Generated by Django 3.2.9 on 2021-12-14 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('espsensor', '0014_auto_20211214_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensorlist',
            name='AirSensor',
            field=models.FloatField(blank=True, default=-1),
        ),
        migrations.AlterField(
            model_name='sensorlist',
            name='CO2',
            field=models.FloatField(blank=True, default=-1, null=True),
        ),
        migrations.AlterField(
            model_name='sensorlist',
            name='HumiSensor',
            field=models.FloatField(blank=True, default=-1, null=True),
        ),
        migrations.AlterField(
            model_name='sensorlist',
            name='LightSensor',
            field=models.FloatField(blank=True, default=-1),
        ),
        migrations.AlterField(
            model_name='sensorlist',
            name='SoilMoistureSensor1',
            field=models.FloatField(blank=True, choices=[('1', 'Active'), ('-1', 'Disable')], default='1', null=True),
        ),
        migrations.AlterField(
            model_name='sensorlist',
            name='SoilMoistureSensor2',
            field=models.FloatField(blank=True, default=-1),
        ),
        migrations.AlterField(
            model_name='sensorlist',
            name='TempSensor',
            field=models.FloatField(blank=True, default=-1, null=True),
        ),
    ]