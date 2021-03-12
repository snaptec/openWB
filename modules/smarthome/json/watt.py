#!/usr/bin/python3
import sys
import os
import time
import json
import jq
import urllib.request

named_tuple = time.localtime() # getstruct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S json watty.py", named_tuple)

devicenumber=str(sys.argv[1])
jsonurl=str(sys.argv[2])      #Abfrage-URL, die die .json Antwort liefert. Z.B. "http://192.168.0.150/solar_api/v1/GetMeterRealtimeData.cgi?Scope=Device&DeviceID=1"
jsonpower=str(sys.argv[3])    #json Key in dem der aktuelle Leistungswert steht, z.B. ".Body.Data.PowerReal_P_Sum"
jsonpowerc=str(sys.argv[4])   #json Key in dem der summierte Verbrauch steht, z.B. ".Body.Data.EnergyReal_WAC_Sum_Consumed"

answer = json.loads(str(urllib.request.urlopen(jsonurl, timeout=3).read().decode("utf-8")))

power = jq.compile(jsonpower).input(answer).first()
powerc = jq.compile(jsonpowerc).input(answer).first()

try:
    power = int(abs(power))
except:
    power = 0
    
try:
    powerc = int(abs(powerc))
except:
    powerc = 0

f1 = open('/var/www/html/openWB/ramdisk/smarthome_device_ret' + str(devicenumber), 'w')
answer = '{"power":' + str(power) + ',"powerc":' + str(powerc) + '}'
json.dump(answer, f1)
f1.close()
