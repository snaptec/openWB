#!/usr/bin/python3
import sys
import time
import json
import urllib.request
named_tuple = time.localtime()  # getstruct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S tasmota watty.py", named_tuple)
devicenumber = str(sys.argv[1])
ipadr = str(sys.argv[2])
uberschuss = int(sys.argv[3])
relais = 0
try:
    answer2 = json.loads(str(urllib.request.urlopen("http://"+str(ipadr) +
                         "/cm?cmnd=Status", timeout=3).read().decode("utf-8")))
    r_status = int(answer2['Status']['Power'])
except Exception:
    r_status = 0
answer = json.loads(str(urllib.request.urlopen("http://"+str(ipadr) +
                    "/cm?cmnd=Status%208", timeout=3).read().decode("utf-8")))
try:
    aktpower = int(answer['StatusSNS']['ENERGY']['Power'])
except Exception:
    aktpower = 0
if (aktpower > 50) or (r_status == 1):
    relais = 1
powerc = 0
answer = '{"power":' + str(aktpower) + ',"powerc":' + str(powerc) + ',"on":' + str(relais) + '} '
f1 = open('/var/www/html/openWB/ramdisk/smarthome_device_ret' + str(devicenumber), 'w')
json.dump(answer, f1)
f1.close()
