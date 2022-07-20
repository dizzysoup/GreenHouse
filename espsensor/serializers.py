from django.contrib.admin import filters
from django.db import models, connection
from django.db.models import fields
from rest_framework import serializers
from espsensor.models import ESP , GREENHOUSE , SENSORLIST

class ESPSerializer(serializers.ModelSerializer):
    class Meta :
        model = ESP
        fields = ("Esp_id","Esp_name","Status")

class GreenHouseSerializer(serializers.ModelSerializer):
    Esp_sensor = ESPSerializer(many = True , read_only = True )
    class Meta : 
        model = GREENHOUSE
        fields = ("Gh_no","Esp_sensor")


    

# class SoilSerializer(serializers.ModelSerializer):
#     class Meta :
#         model = SOIL
#         fields = ('created','soil_no', 'soil_degree')

# class LightSerializer(serializers.ModelSerializer):
#     class Meta : 
#         model = LIGHT
#         fields = ('light_degree', 'created')

# class ESPSerializer(serializers.ModelSerializer):    
#     soil = SoilSerializer(many = True , read_only = True)
#     light = LightSerializer(many = True , read_only = True)

#     class Meta:
#         model = ESP
#         fields = ('name', 'soil','light')

# class ESPSensorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ESP
#         fields = ('esp_id' , 'name')

