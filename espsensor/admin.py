from django.contrib import admin
from django.contrib.admin.decorators import display, register

# Register your models here.
from .models import ESP , SOIL , LIGHT


class ESPAdmin(admin.ModelAdmin):
    list_display = ("esp_id" , "name")

class SoilAdmin(admin.ModelAdmin):
    list_display = ("serial_id","esp_id",'soil_no','soil_degree' , "created")

class LightAdmin(admin.ModelAdmin):
    list_display = ("serial_id", "esp_id", "light_degree" , "created")

admin.site.register(ESP,ESPAdmin)
admin.site.register(SOIL, SoilAdmin)
admin.site.register(LIGHT, LightAdmin)
