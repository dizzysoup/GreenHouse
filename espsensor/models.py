from django.db import models

# Create your models here.
class ESP(models.Model) : 
    esp_id = models.IntegerField(blank=True,primary_key=True)
    name = models.CharField(max_length=50)
    GH_no = models.IntegerField(blank = True , null = False , default = 1 ) 
   

   
class LIGHT(models.Model):
    serial_id = models.AutoField(primary_key=True)
    light_degree = models.FloatField(null=True, blank=True, default= 0)
    created = models.DateTimeField(auto_now_add= True , null = True )
    esp_id = models.ForeignKey("ESP",related_name='light', on_delete=models.CASCADE)


class SOIL(models.Model):
    serial_id = models.AutoField(primary_key=True)
    soil_degree = models.FloatField(null = True , blank = True , default = 0)
    soil_no = models.IntegerField(null = True , blank = True , default = 0 )
    created = models.DateTimeField(auto_now_add=True , null = True )
    esp_id = models.ForeignKey("ESP",related_name='soil' , on_delete=models.CASCADE)

class Temp(models.Model):
    serial_id = models.AutoField(primary_key=True)
    temp_degree =  models.FloatField(null = True , blank = True , default = 0 )
    esp_id = models.ForeignKey("ESP" , on_delete=models.CASCADE)    

def sql_query(**kwargs):
    esp_id = kwargs.get('esp_id')
    if esp_id:
        result = ESP.objects.raw('select *from espsensor_esp where esp_id = %s' , [esp_id])
    else :
        result = ESP.objects.raw('select esp_id, name from espsensor_esp')
    return result