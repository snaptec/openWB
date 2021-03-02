#!/usr/bin/python3
import sys
import os
import time
import json
import urllib.request

named_tuple = time.localtime() # getstruct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S json watty.py", named_tuple)

devicenumber=str(sys.argv[1])
getstring=str(sys.argv[2])      #Abfragestring, der die .json Antwort liefert. Z.B. "http://192.168.0.150/solar_api/v1/GetMeterRealtimeData.cgi?Scope=Device&DeviceID=1"
powerstring=int(sys.argv[3])    #json Key in dem der aktuelle Leistungswert steht, mit Punkt am Anfang. Z.B. ".Body.Data.PowerRealtime_P_Sum"
powercstring=int(sys.argv[4])   #json Key in dem der summierte Verbrauch steht, mit Punkt am Anfang. Z.B. ".Body.Data.EnergyReal_WAC_Sum_Consumed"

answer = json.loads(str(urllib.request.urlopen(getstring, timeout=3).read().decode("utf-8")))

powerlist = powerstring.split(".")
powerclist = powercstring.split(".")

if len(powerlist) <=7:
    if len(powerlist) == 2:
        power = answer[powerlist[1]]
    elif len(powerlist) == 3:
        power = answer[powerlist[1]][powerlist[2]]
    elif len(powerlist) == 4:
        power = answer[powerlist[1]][powerlist[2]][powerlist[3]]
    elif len(powerlist) == 5:
        power = answer[powerlist[1]][powerlist[2]][powerlist[3]][powerlist[4]]
    elif len(powerlist) == 6:
        power = answer[powerlist[1]][powerlist[2]][powerlist[3]][powerlist[4]][powerlist[5]]
    elif len(powerlist) == 7:
        power = answer[powerlist[1]][powerlist[2]][powerlist[3]][powerlist[4]][powerlist[5]][powerlist[6]]

if len(powerclist) <=7:
    if len(powerclist) == 2:
        powerc = answer[powerclist[1]]
    elif len(powerlist) == 3:
        powerc = answer[powerclist[1]][powerclist[2]]
    elif len(powerlist) == 4:
        powerc = answer[powerclist[1]][powerclist[2]][powerclist[3]]
    elif len(powerlist) == 5:
        powerc = answer[powerclist[1]][powerclist[2]][powerclist[3]][powerclist[4]]
    elif len(powerlist) == 6:
        powerc = answer[powerclist[1]][powerclist[2]][powerclist[3]][powerclist[4]][powerclist[5]]
    elif len(powerlist) == 7:
        powerc = answer[powerclist[1]][powerclist[2]][powerclist[3]][powerclist[4]][powerclist[5]][powerclist[6]]

power=abs(power)
powerc=abs(powerc)
answer = '{"power":' + str(power) + ',"powerc":' + str(powerc) + '} '

f1 = open('/var/www/html/openWB/ramdisk/smarthome_device_ret' + str(devicenumber), 'w')
json.dump(answer,f1)
f1.close()
