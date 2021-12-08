from django.db.models.query import QuerySet
from rest_framework.decorators import action
from django.core import serializers
from rest_framework.views import APIView
from espsensor.serializers import ESPSerializer , ESPSensorSerializer
from espsensor.models import ESP
from espsensor.models import sql_query
from rest_framework import serializers, viewsets , status
from rest_framework.response import Response

import json

class ESPViewSet(viewsets.ModelViewSet):
    queryset = ESP.objects.all()
    serializer_class = ESPSensorSerializer

    @action(detail = False , methods=['get'], url_path = 'history')
    def history(self, request): 
        esp_id = request.query_params.get('esp_id' , None)
        queryset = sql_query(esp_id = esp_id)
        serializer_class = ESPSerializer(queryset , many = True)
        return Response(serializer_class.data , status = status.HTTP_200_OK)


  