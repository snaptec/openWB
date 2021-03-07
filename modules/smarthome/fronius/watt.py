#!/usr/bin/python3
import sys
import os
import time
import json
import urllib.request

named_tuple = time.localtime() # getstruct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S fronius watty.py", named_tuple)

devicenumber=str(sys.argv[1])
ipadr=str(sys.argv[2])        #IP-ADresse des Fronius Wechselrichters, mit dem der Zähler kommuniziert
smid=int(sys.argv[3])         #ID des Zählers im Wechselrichter (Hauptzähler 0, weitere fortlaufend)

answer = json.loads(str(urllib.request.urlopen("http://"+str(ipadr)+"/solar_api/v1/GetMeterRealtimeData.cgi?Scope=Device&DeviceID="+str(smid), timeout=3).read().decode("utf-8")))
try:
 power = answer['Body']['Data']['PowerReal_P_Sum']
 power = int(abs(power))
except:
 power = 0

try:
 powerc = answer['Body']['Data']['EnergyReal_WAC_Sum_Consumed']
 powerc = int(abs(powerc))
except:
 powerc = 0
 
f1 = open('/var/www/html/openWB/ramdisk/smarthome_device_ret' + str(devicenumber), 'w')
answer = '{"power":' + str(power) + '}{"powerc":' + str(powerc) + '} '
json.dump(answer, f1)
f1.close()
