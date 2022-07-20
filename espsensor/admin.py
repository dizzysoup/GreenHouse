from dataclasses import fields
from django.contrib import admin
from django.contrib.admin.decorators import display, register
from django.contrib.admin.views.main import ChangeList
from espsensor.models import SENSORLIST, GREENHOUSE , SOIL , TEMP , AIR , CO2 , HUMI , LIGHT , ESP
from django.utils.html import format_html 


class EspAdmin(admin.ModelAdmin):
    list_display = ("Esp_name" , "Status" , "get_GH")
    def get_GH(self , obj) : 
        return obj.GH_id
    
    get_GH.short_description = "溫室編號" 
    get_GH.admin_order_field = "GH_id__Gh_no"


class GreenHouseAdmin(admin.ModelAdmin):
    list_display = ("Serial_id","Gh_no")

class SensorAdmin(admin.ModelAdmin):
    show_element = ('get_esp' , 'get_GH' , 
    'Soil_1' , 'Soil_2' ,'Light','Air','Temp','Humi','CO2')
    list_display = show_element
    
    fields = ('ESPSerial',
        'SoilMoistureSensor1','SoilMoistureSensor2','LightSensor','AirSensor','TempSensor','HumiSensor','CO2Sensor')
    
    ordering = ('ESPSerial__Esp_name',)

    def get_esp(self , obj ):
        Esp_name = obj.ESPSerial.Esp_name        
        return   Esp_name
    def get_GH(self , obj):
        return obj.ESPSerial.GH_id      
 
    get_esp.short_description = 'ESP'
    get_esp.admin_order_field = 'ESPSerial__Esp_name'
    get_GH.short_description = 'GH'

class SoilAdmin(admin.ModelAdmin):
    list_display = ('get_esp', 'get_gh', 'Soil_no','Soil_degree','Created')

    def get_esp(self , obj ):
        return obj.EspSerial.Esp_name
    
    def get_gh(self,obj):
        return obj.EspSerial.GH_id
    
    get_esp.short_description = 'ESP'
    get_esp.admin_order_field = 'EspSerial__Esp_name'
    get_gh.short_description = '溫室編號'

class TempAdmin(admin.ModelAdmin):
    list_display = ('get_esp', 'get_gh','Temp_degree','Created')

    def get_esp(self , obj ):
        return obj.EspSerial.Esp_name
    
    def get_gh(self,obj):
        return obj.EspSerial.GH_id
    
    get_esp.short_description = 'ESP'
    get_esp.admin_order_field = 'EspSerial__Esp_name'
    get_gh.short_description = 'GH'

class AirAdmin(admin.ModelAdmin):
    list_display = ('get_esp', 'get_gh','Pm25_degree','Created')

    def get_esp(self , obj ):
        return obj.EspSerial.Esp_name
    
    def get_gh(self,obj):
        return obj.EspSerial.GH_id
    
    get_esp.short_description = 'ESP'
    get_esp.admin_order_field = 'EspSerial__Esp_name'
    get_gh.short_description = 'GH'

class CO2Admin(admin.ModelAdmin):
    list_display = ('get_esp', 'get_gh','Co2_degree','Created')

    def get_esp(self , obj ):
        return obj.EspSerial.Esp_name
    
    def get_gh(self,obj):
        return obj.EspSerial.GH_id
    
    get_esp.short_description = 'ESP'
    get_esp.admin_order_field = 'EspSerial__Esp_name'
    get_gh.short_description = 'GH'

class HumiAdmin(admin.ModelAdmin):
    list_display = ('get_esp', 'get_gh','Humi_degree','Created')

    def get_esp(self , obj ):
        return obj.EspSerial.Esp_name
    
    def get_gh(self,obj):
        return obj.EspSerial.GH_id
    
    get_esp.short_description = 'ESP'
    get_esp.admin_order_field = 'EspSerial__Esp_name'
    get_gh.short_description = 'GH'

class LightAdmin(admin.ModelAdmin):
    list_display = ('get_esp', 'get_gh','Light_degree','Created')

    def get_esp(self , obj ):
        return obj.EspSerial.Esp_name
    
    def get_gh(self,obj):
        return obj.EspSerial.GH_id
    
    get_esp.short_description = 'ESP'
    get_esp.admin_order_field = 'EspSerial__Esp_name'
    get_gh.short_description = 'GH'

class ESPSelect(ChangeList):
    def get_query_set(self , request):
        qs = super()

admin.site.register(SENSORLIST , SensorAdmin)
admin.site.register(SOIL ,SoilAdmin)
admin.site.register(TEMP ,TempAdmin)
admin.site.register(CO2, CO2Admin)
admin.site.register(AIR, AirAdmin)
admin.site.register(HUMI, HumiAdmin)
admin.site.register(LIGHT, LightAdmin)
admin.site.register(GREENHOUSE , GreenHouseAdmin)
admin.site.register(ESP,EspAdmin)
