#!/usr/bin/python3
import sys
import os
import time
import json
import urllib.request

named_tuple = time.localtime() # getstruct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S fronius watty.py", named_tuple)

devicenumber=str(sys.argv[1])
ipadr=str(sys.argv[2])
smid=int(sys.argv[3])

answer = json.loads(str(urllib.request.urlopen("http://"+str(ipadr)+"/solar_api/v1/GetMeterRealtimeData.cgi?Scope=Device&DeviceID="+str(smid), timeout=3).read().decode("utf-8")))
aktpower = answer['Body']['Data']['PowerReal_P_Sum']*-1
powerc = answer['Body']['Data']['EnergyReal_WAC_Sum_Consumed']

#if aktpower > 50:
#    relais = 1
#else:
#    relais = 0

answer = '{"power":' + str(aktpower) + ',"powerc":' + str(powerc)  + '} '
#answer = '{"power":' + str(aktpower) + ',"powerc":' + str(powerc) + ',"on":' + str(relais) + '} '
f1 = open('/var/www/html/openWB/ramdisk/smarthome_device_ret' + str(devicenumber), 'w')
json.dump(answer,f1)
f1.close()
