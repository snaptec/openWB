#!/usr/bin/python3
import sys
import time
import json
import jq
import urllib.request
named_tuple = time.localtime()  # getstruct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S tasmota watty.py", named_tuple)
devicenumber = str(sys.argv[1])
ipadr = str(sys.argv[2])
uberschuss = int(sys.argv[3])
relais = 0
jsonurl1 = "http://"+str(ipadr)+"/cm?cmnd=Status"
jsonurl2 = "http://"+str(ipadr)+"/cm?cmnd=Status%208"
jsonpow = ".Status.Power"

try:
    answer = json.loads(str(urllib.request.urlopen(jsonurl1, timeout=3).read().decode("utf-8")))
    p_status = jq.compile(jsonpow).input(answer).first()
    if type(p_status) is int:
        relais = p_status % 2
    elif type(p_status) is str:
        relais  = int(p_status, 2) % 2
    else:
        relais = 0
except Exception:
    relais = 0

try:
    answer = json.loads(str(urllib.request.urlopen(jsonurl2, timeout=3).read().decode("utf-8")))
    aktpower = int(answer['StatusSNS']['ANALOG']['CTEnergy']['Power'])
    powerc = int((answer['StatusSNS']['ANALOG']['CTEnergy']['Energy']) * 1000)
except Exception:
    aktpower = 0
    powerc = 0

answer = '{"power":' + str(aktpower) + ',"powerc":' + str(powerc) + ',"on":' + str(relais) + '} '
f1 = open('/var/www/html/openWB/ramdisk/smarthome_device_ret' + str(devicenumber), 'w')
json.dump(answer, f1)
f1.close()
