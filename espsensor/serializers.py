from rest_framework import serializers
from espsensor.models import ESP , SOIL , LIGHT



class SoilSerializer(serializers.ModelSerializer):
    class Meta :
        model = SOIL
        fields = ('created','soil_no', 'soil_degree')

class LightSerializer(serializers.ModelSerializer):
    class Meta : 
        model = LIGHT
        fields = ('light_degree', 'created')

class ESPSerializer(serializers.ModelSerializer):    
    soil = SoilSerializer(many = True , read_only = True)
    light = LightSerializer(many = True , read_only = True)

    class Meta:
        model = ESP
        fields = ('name', 'soil','light')

class ESPSensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ESP
        fields = ('esp_id' , 'name')

