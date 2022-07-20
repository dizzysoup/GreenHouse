from rest_framework import views
from django.db import connection
from django.db.models import Q
from django.views.generic.list import ListView
from rest_framework import decorators
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from espsensor.serializers import ESPSerializer , GreenHouseSerializer
from espsensor.models import ESP, GREENHOUSE , SOIL , LIGHT , AIR , TEMP , HUMI , CO2
from rest_framework import serializers, viewsets , status
from rest_framework.response import Response


ESP_list = ["ESP11","ESP12","ESP21","ESP22","ESP31","ESP32","ESP41","ESP42"]

class GreenViewSet(viewsets.ModelViewSet):
    queryset = GREENHOUSE.objects.all()
    serializer_class = GreenHouseSerializer


@api_view(['GET' , 'POST'])
def api_sensor(request , nodename):       
    #GET 的狀況
    if (request.method == "GET") :
        query = '''
            select distinct p.Esp_name,p.`Status` ,
              s.SoilMoistureSensor1 , s.SoilMoistureSensor2,
              s.LightSensor  , s.AirSensor , s.TempSensor , s.HumiSensor , s.CO2Sensor
            from sensorlist s 
            inner join 
            esp p 
            on s.ESPSerial_id = p.Serial_id
            inner join 
            greenhouse g 
            on g.Serial_id = p.GH_id
            and GH_no = %s             
        '''         
        try :
            cursor = connection.cursor()
            cursor.execute(query , str(nodename))
            data = cursor.description
            rows = cursor.fetchall()            
            result = { "Nodename" : nodename }
            for row in rows :                  
                tmp = dict(zip([column[0] for column in data] , row))
                if tmp['SoilMoistureSensor1'] == -1 :
                    del tmp['SoilMoistureSensor1']
                if tmp['SoilMoistureSensor2'] == -1 :
                    del tmp['SoilMoistureSensor2']
                if tmp['LightSensor'] == -1 :
                    del tmp['LightSensor']
                if tmp['AirSensor'] == -1 :
                    del tmp['AirSensor']
                if tmp['TempSensor'] == -1 :
                    del tmp['TempSensor']
                if tmp['HumiSensor'] == -1 :
                    del tmp['HumiSensor']
                if tmp['CO2Sensor'] == -1 :
                    del tmp['CO2Sensor']
                result[tmp.get("Esp_name")] = tmp        

            # result = [dict(zip([column[0] for column in data] , row)) for row in rows]
        finally :
            cursor.close()
        return Response(result , status=status.HTTP_200_OK)
    #POST 的狀況
    elif (request.method == "POST") :
        try :
            cursor = connection.cursor()
            nodename = request.data.get("Nodename")
            for esp in ESP_list :
                data = request.data.get(esp) 
                if data == None : continue                            
                esp_name = data['Esp_name']               
                cursor.execute("select Serial_id from esp where esp_name = %s and GH_id = %s " , [esp_name, nodename])
                serial_id = cursor.fetchone() # esp_name 所在位置   
                if 'SoilMoistureSensor1' in data :
                    SOIL.objects.create(Soil_degree=data['SoilMoistureSensor1'],Soil_no = 1,EspSerial_id = serial_id[0])                  
                if 'SoilMoistureSensor2' in data :    
                    SOIL.objects.create(Soil_degree=data['SoilMoistureSensor2'] ,Soil_no = 2,EspSerial_id = serial_id[0])        
                if 'LightSensor' in data :
                    LIGHT.objects.create(Light_degree=data['LightSensor'],EspSerial_id = serial_id[0])
                if 'AirSensor' in data :
                    AIR.objects.create(Pm25_degree = data['AirSensor'],EspSerial_id = serial_id[0])
                if 'TempSensor' in data : 
                    TEMP.objects.create(Temp_degree = data['TempSensor'] , EspSerial_id = serial_id[0])
                if 'HumiSensor' in data :
                    HUMI.objects.create(Humi_degree = data['HumiSensor'] , EspSerial_id = serial_id[0])
                if 'CO2Sensor' in data :
                    CO2.objects.create(Co2_degree = data['CO2Sensor'] , EspSerial_id = serial_id[0])
                                
        finally :
            cursor.close()
        return  Response(request.data , status=status.HTTP_200_OK)

def get_soil(esp , time  , soil_no , datestart = 0 , dateend = 0 ):
    query = '''
        select  '土壤濕度' as Title , Soil_degree as Value ,convert(Created , char(16)) as Created , "%%" as Type 
        from soil where EspSerial_id = %s and Soil_no = %s  
    '''
    if datestart != 0 and dateend != 0 :
        start = str(datestart)[0:4] + "-" + str(datestart)[4:6] + "-" + str(datestart)[6:]
        end = str(dateend)[0:4] + "-" + str(dateend)[4:6] + "-" + str(dateend)[6:]
        query += " and convert(Created , char(10))  between '" + start+ "' and '" + end +"'"
    
    query += ' order by Created desc '
    if time == 1 : query += "limit 1 "

    cursor = connection.cursor()
    cursor.execute(query , [str(esp) , str(soil_no)])
    data = cursor.description 
    rows = cursor.fetchall()
    res = {}
    for row in rows : 
        if time == 1 :
            res = dict(zip([column[0] for column in data] , row))        
        else :
            res[row[0]] = row[1]
    return res


def get_data(esp, time , tbname , datestart = 0 , dateend = 0 ):
    if tbname == 'light' : 
        title = "'光照'"
        type = "'%%'"
    elif tbname == 'temp' : 
        title = "'環境溫度'"                                                           
        type = "'°C'"
    elif tbname == 'co2' : 
        title = "'二氧化碳'"
        type = "'ppm'"
    elif tbname == 'humi' : 
        title = "'土壤酸鹼值'"
        type = "'%%'"
    elif tbname == 'air' : 
        title = "'空氣濕度'"
        type = "'%%'"
    query = '''
        select ''' + title + ''' as Title , ''' + tbname + '''_degree as Value  , ''' + type + ''' as Type ,convert(Created , char(16)) as Created 
        from 
    '''
    query += tbname 
    query += '''
        where EspSerial_id = %s 
    '''
    if datestart != 0 and dateend != 0 :
        start = str(datestart)[0:4] + "-" + str(datestart)[4:6] + "-" + str(datestart)[6:]
        end = str(dateend)[0:4] + "-" + str(dateend)[4:6] + "-" + str(dateend)[6:]
        query += " and convert(Created , char(10))  between '" + start+ "' and '" + end +"'"
    query += " order by Created desc "
    if time == 1 : query += " limit 1 "
    cursor = connection.cursor()
    cursor.execute(query , str(esp))
    data = cursor.description
    rows = cursor.fetchall()
    res = {}
    for row in rows : 
        if time == 1 :
            res = dict(zip([column[0] for column in data] , row))        
        else :
            res[row[0]] = row[1]
    return res

def get_air(esp, time , datestart = 0  , dateend = 0  ):
    query = '''
        select '光照' as Title ,Pm25_degree,convert(Created , char(16)) as Created 
        from air
        where EspSerial_id = %s 
    '''
    if datestart != 0 and dateend != 0 :
        start = str(datestart)[0:4] + "-" + str(datestart)[4:6] + "-" + str(datestart)[6:]
        end = str(dateend)[0:4] + "-" + str(dateend)[4:6] + "-" + str(dateend)[6:]
        query += " and convert(Created , char(10))  between '" + start+ "' and '" + end +"'"
    query += ' order by Created desc '
    if time == 1 : query += " limit 1 "
    cursor = connection.cursor()
    cursor.execute(query , str(esp))
    data = cursor.description
    rows = cursor.fetchall()
    res = {}
    for row in rows : 
        if time == 1 :
            res = dict(zip([column[0] for column in data] , row))        
        else :
            res[row[0]] = row[1]
    return res


@api_view(['GET'])
def api_now(request ,nodename , esp ):    
    chk_query = '''
        select  p.Serial_id as esp_id , s.*        
        from esp p inner join sensorlist s 
        on p.Esp_name = %s and p.Serial_id = s.ESPSerial_id 
        and p.GH_id = %s 
    '''
    espname = 'ESP' + str(esp);
    cursor  = connection.cursor()
    cursor.execute(chk_query , [espname,str(nodename)])
    data = cursor.description
    rows = cursor.fetchall()
    
    res = {}
    
    for row in rows :
        tmp = dict(zip([column[0] for column in data] , row))
        esp_id = tmp['esp_id']
        if tmp['SoilMoistureSensor1'] == 1 :
            res['soil1'] = get_soil(esp_id, 1 , 1  )
        if tmp['SoilMoistureSensor2'] == 1 :
            res['soil2'] = get_soil(esp_id , 1,1 )
        if tmp['TempSensor'] == 1 :
            res['temp'] = get_data(esp_id , 1 , 'temp')
        if tmp['CO2Sensor'] == 1 :
            res['co2'] = get_data(esp_id, 1 ,'co2')
        if tmp['LightSensor'] == 1 :
            res['light'] = get_data(esp_id , 1 , 'light' )
        if tmp['HumiSensor'] == 1 :
            res['humi'] = get_data(esp_id , 1 , 'humi')
        if tmp['AirSensor'] == 1 :
            res['air'] = get_air(esp_id ,1)

    return Response(res , status=status.HTTP_200_OK)

@api_view(['GET'])
def api_history(request ,nodename , esp , datestart = 0 , dateend = 0 ):       
    chk_query = '''
        select  p.Serial_id as esp_id , s.*
        from esp p inner join sensorlist s
        on p.Esp_id = %s and p.Serial_id = s.ESPSerial_id 
        and p.GH_id = %s 
    '''
    cursor  = connection.cursor()
    cursor.execute(chk_query , [str(esp),str(nodename)])
    data = cursor.description
    rows = cursor.fetchall()    
    res = {}
    #res["ESP"] = esp 
    for row in rows :
        tmp = dict(zip([column[0] for column in data] , row))
        esp_id = tmp['esp_id']
        if tmp['SoilMoistureSensor1'] == 1 :
            res['soil1'] = get_soil(esp_id,0,1, datestart , dateend)
        if tmp['SoilMoistureSensor2'] == 1 :
            res['soil2'] = get_soil(esp_id,0,2, datestart , dateend)
        if tmp['TempSensor'] == 1 :
            res['temp'] = get_data(esp_id,0,'temp', datestart , dateend)
        if tmp['CO2Sensor'] == 1 :
            res['co2'] = get_data(esp_id,0,'co2', datestart , dateend)
        if tmp['LightSensor'] == 1 :
            res['light'] = get_data(esp_id,0,'light', datestart , dateend )
        if tmp['HumiSensor'] == 1 :
            res['humi'] = get_data(esp_id,0,'humi', datestart , dateend)
        if tmp['AirSensor'] == 1 :
            res['air'] = get_air(esp_id,0, datestart , dateend)

    return Response(res , status=status.HTTP_200_OK)

# class ESPViewSet(viewsets.ModelViewSet):
#     queryset = ESP.objects.all()
#     serializer_class = ESPSensorSerializer

#     @action(detail = False , methods=['get'], url_path = 'history')
#     def history(self, request): 
#         esp_id = request.query_params.get('esp_id' , None)
#         queryset = sql_query(esp_id = esp_id)
#         serializer_class = ESPSerializer(queryset , many = True)
#         return Response(serializer_class.data , status = status.HTTP_200_OK)


  