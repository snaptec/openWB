#!/usr/bin/python3
import sys
import os
import time
import json
import urllib.request

def get_nested_value(input_dict, nested_key):
    internal_dict_value = input_dict
    for k in nested_key:
        try:
            internal_dict_value = internal_dict_value.get(k)
        except:
            return None
    return internal_dict_value

named_tuple = time.localtime() # getstruct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S json watty.py", named_tuple)

devicenumber=str(sys.argv[1])
getstring=str(sys.argv[2])      #Abfragestring, der die .json Antwort liefert. Z.B. "http://192.168.0.150/solar_api/v1/GetMeterRealtimeData.cgi?Scope=Device&DeviceID=1"
powerstring=int(sys.argv[3])    #json Key in dem der aktuelle Leistungswert steht, z.B. "Body.Data.PowerReal_P_Sum"
powercstring=int(sys.argv[4])   #json Key in dem der summierte Verbrauch steht, z.B. "Body.Data.EnergyReal_WAC_Sum_Consumed"

if "*" in powerstring:
    powerrechnung = powerstring.split("*")
    try:
        powerfaktor = float(powerrechnung[0])
        powerstring = powerrechnung[1]
    except:
        powerfaktor = float(powerrechnung[1])
        powerstring = powerrechnung[0]

if "*" in powercstring:
    powercrechnung = powercstring.split("*")
    try:
        powercfaktor = float(powercrechnung[0])
        powercstring = powercrechnung[1]
    except:
        powercfaktor = float(powercrechnung[1])
        powercstring = powercrechnung[0]

answer = json.loads(str(urllib.request.urlopen(getstring, timeout=3).read().decode("utf-8")))

powerlist = list(filter(None, powerstring.split(".")))   # entferne leere Einträge
powerclist = list(filter(None, powercstring.split("."))) # entferne leere Einträge

power = get_nested_value(answer, powerlist)
powerc = get_nested_value(answer, powerclist)

try:
    power = int(abs(powerfaktor*power))
except:
    power = 0
    
try:
    powerc = int(abs(powercfaktor*powerc))
except:
    powerc = 0

f1 = open('/var/www/html/openWB/ramdisk/smarthome_device_ret' + str(devicenumber), 'w')
answer = '{"power":' + str(power) + ',"powerc":' + str(powerc) + '}'
json.dump(answer, f1)
f1.close()
