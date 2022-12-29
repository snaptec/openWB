#!/usr/bin/python3
import sys
import time
import json
import urllib.request
named_tuple = time.localtime()  # getstruct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S mystrom watty.py", named_tuple)
devicenumber = str(sys.argv[1])
ipadr = str(sys.argv[2])
uberschuss = int(sys.argv[3])
answer = json.loads(str(urllib.request.urlopen("http://"+str(ipadr)+"/report", timeout=3).read().decode("utf-8")))
aktpower = int(answer['power'])
relaiss = str(answer['relay'])
if (relaiss.lower() == "true"):
    relais = 1
else:
    relais = 0
templong = str(float(answer['temperature']))
temp = templong[0:5]
powerc = 0
answer = '{"power":' + str(aktpower) + ',"powerc":' + str(powerc) + ',"on":' + \
    str(relais) + ',"temp0":' + str(temp) + '} '
f1 = open('/var/www/html/openWB/ramdisk/smarthome_device_ret' + str(devicenumber), 'w')
json.dump(answer, f1)
f1.close()
