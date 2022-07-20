from django.db import models , connection
from django.db.models.deletion import CASCADE
from django.utils.html import format_html
from django import forms
# Create your models here.



class GREENHOUSE(models.Model) :
    Serial_id = models.AutoField(primary_key=True)
    Gh_no = models.IntegerField(blank = True , null = False , default = 1 ) 
    class Meta :
        db_table = 'greenhouse'
    
    def __str__(self):
        return str(self.Gh_no)

ACTIVE_CHOICE = (
    (1,'Active'),
    (-1,'Disable'),   
) 



class SENSORLIST(models.Model):
    Serial_id = models.AutoField(primary_key=True)        
    ESPSerial = models.ForeignKey("ESP",related_name="Esp_Sensor", on_delete=CASCADE)
    SoilMoistureSensor1 = models.FloatField(blank = True , null = False ,choices=ACTIVE_CHOICE, default = 1)
    SoilMoistureSensor2 = models.FloatField(blank = True , null = False ,choices=ACTIVE_CHOICE ,default = -1 )
    LightSensor = models.FloatField(blank = True , null = False ,choices=ACTIVE_CHOICE ,default = -1 )
    AirSensor = models.FloatField(blank = True , null = False,choices=ACTIVE_CHOICE ,default = -1 )
    TempSensor = models.FloatField(blank=True , null = True,choices=ACTIVE_CHOICE ,default= -1 )
    HumiSensor = models.FloatField(blank=True , null = True,choices=ACTIVE_CHOICE,default = -1 )
    CO2Sensor = models.FloatField(blank = True ,null = True,choices=ACTIVE_CHOICE, default = -1 )

    class Meta:
        db_table = 'sensorlist'

    def Soil_1(self):
        name = 'Active' if self.SoilMoistureSensor1 == 1 else 'Disable'
        color_code = 'green' if self.SoilMoistureSensor1 == 1 else 'red'     
        return format_html(
            '<span style="color: {};"> {} </span>',
            color_code,
            name
        )
    def Soil_2(self):
        name = 'Active' if self.SoilMoistureSensor2 == 1 else 'Disable'
        color_code = 'green' if self.SoilMoistureSensor2 == 1 else 'red'     
        return format_html(
            '<span style="color: {};"> {} </span>',
            color_code,
            name
        )
    def Light(self):
        name = 'Active' if self.LightSensor == 1 else 'Disable'
        color_code = 'green' if self.LightSensor == 1 else 'red'
        return format_html(
            '<span style="color: {};"> {} </span>',
            color_code,
            name
        )
    def Temp(self):
        name = 'Active' if self.TempSensor == 1 else 'Disable'
        color_code = 'green' if self.TempSensor == 1 else 'red'
        return format_html(
            '<span style="color: {};"> {} </span>',
            color_code,
            name
        )
    def Air(self):
        name = 'Active' if self.AirSensor == 1 else 'Disable'
        color_code = 'green' if self.AirSensor == 1 else 'red'
        return format_html(
            '<span style="color: {};"> {} </span>',
            color_code,
            name
        )

    def Humi(self):
        name = 'Active' if self.HumiSensor == 1 else 'Disable'
        color_code = 'green' if self.HumiSensor == 1 else 'red'
        return format_html(
            '<span style="color: {};"> {} </span>',
            color_code,
            name
        )
    
    def CO2(self):
        name = 'Active' if self.CO2Sensor == 1 else 'Disable'
        color_code = 'green' if self.CO2Sensor == 1 else 'red'
        return format_html(
            '<span style="color: {};"> {} </span>',
            color_code,
            name
        )

class ESP(models.Model) : 
    Serial_id = models.AutoField(primary_key=True)    
    Esp_name = models.CharField(max_length=50)
    GH = models.ForeignKey("GREENHOUSE", related_name="Esp_sensor",on_delete=models.CASCADE) 
    Status = models.IntegerField(blank = True , null = False , default = 0)      

    class Meta :
        db_table = 'esp'
    
    def __str__(self):
        return str(self.GH) +"/"+self.Esp_name 

class LIGHT(models.Model):
    Serial_id = models.AutoField(primary_key=True)
    Light_degree = models.FloatField(null=True, blank=True, default= 0)
    Created = models.DateTimeField(auto_now_add= True , null = True )
    EspSerial = models.ForeignKey("ESP",related_name='light', on_delete=models.CASCADE)
    

    class Meta  :
        db_table = 'light'

class SOIL(models.Model):
    Serial_id = models.AutoField(primary_key=True)
    Soil_degree = models.FloatField(null = True , blank = True , default = 0)
    Soil_no = models.IntegerField(null = True , blank = True , default = 0 )
    Created = models.DateTimeField(auto_now_add=True , null = True )
    EspSerial = models.ForeignKey("ESP", related_name='soil' , on_delete=models.CASCADE)
    

    def save(self , *args , **kwargs):
        super(SOIL , self).save(*args , **kwargs)
        self.name = str(self.name.encode('unicode_escape'))

    class Meta :
        db_table = 'soil'

class AIR(models.Model):
    Serial_id = models.AutoField(primary_key=True)
    Pm25_degree = models.FloatField(null=True , blank = True , default = 0)
    Created = models.DateTimeField(auto_now_add = True , null = True )
    EspSerial = models.ForeignKey("ESP", related_name='air' , on_delete=models.CASCADE)
   # Title = models.TextField(null = False , blank = False , default = '空氣濕度')
    class Meta : 
        db_table = 'air'

class TEMP(models.Model):
    Serial_id = models.AutoField(primary_key=True)
    Temp_degree = models.FloatField(null = True , blank = True , default = 0 )
    Created = models.DateTimeField(auto_now_add= True , null = True )
    EspSerial = models.ForeignKey("ESP", related_name='temp' , on_delete=models.CASCADE)
    #Title = models.TextField(null = False , blank= False , default = '空氣濕度')
    class Meta :
        db_table = 'temp'


class HUMI(models.Model):
    Serial_id = models.AutoField(primary_key=True)
    Humi_degree = models.FloatField(null = True , blank = True , default = 0 )
    Created = models.DateTimeField(auto_now_add= True , null = True )
    EspSerial = models.ForeignKey("ESP" , related_name='humi' , on_delete=models.CASCADE)
    #Title = models.TextField(null = False , blank=False , default = '')
    class Meta :
        db_table = 'humi'

class CO2(models.Model):
    Serial_id = models.AutoField(primary_key=True)
    Co2_degree = models.FloatField(null = True , blank = True , default = 0 )
    Created = models.DateTimeField(auto_now_add= True , null = True )
    EspSerial = models.ForeignKey("ESP" , related_name='co2' , on_delete=models.CASCADE)
    #Title = models.TextField(null = False , blank = False , default = '二氧化碳')
    class Meta :
        db_table = 'co2'

class MQTT(models.Model):
    Serial_id = models.AutoField(primary_key=True)
    Fan = models.BooleanField(null = False , blank= True , default = 0 )

    class Meta :
        db_table = 'mqtt'

# def sql_query(**kwargs):
#     esp_id = kwargs.get('esp_id')
#     if esp_id:
#         result = ESP.objects.raw('select *from espsensor_esp where esp_id = %s' , [esp_id])
#     else :
#         result = ESP.objects.raw('select esp_id, name from espsensor_esp')
#     return result

