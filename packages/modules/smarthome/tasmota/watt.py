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
#jsonurl0 = "http://"+str(ipadr)+"/cm?cmnd=Status"
jsonurl1 = "http://"+str(ipadr)+"/cm?cmnd=Status%2011"
jsonurl2 = "http://"+str(ipadr)+"/cm?cmnd=Status%208"
jsonpow = ".StatusSTS.POWER"
jsonpow1 = ".StatusSTS.POWER1"

try:
    answer = json.loads(str(urllib.request.urlopen(jsonurl1, timeout=3).read().decode("utf-8")))
    p_status = jq.compile(jsonpow).input(answer).first()
    #p_status = int((answer['Status']['Power']) % 2)
    if p_status == None:
        p_status = jq.compile(jsonpow1).input(answer).first()
    if p_status == None:
        p_status = "OFF"
except Exception:
    p_status = "OFF"

try:
    answer = json.loads(str(urllib.request.urlopen(jsonurl2, timeout=3).read().decode("utf-8")))
    aktpower = int(answer['StatusSNS']['ANALOG']['CTEnergy']['Power'])
    powerc = int((answer['StatusSNS']['ANALOG']['CTEnergy']['Energy']) * 1000)
except Exception:
    aktpower = 0
    powerc = 0

if (aktpower > 50) or (p_status == "ON"):
    relais = 1
answer = '{"power":' + str(aktpower) + ',"powerc":' + str(powerc) + ',"on":' + str(relais) + '} '
f1 = open('/var/www/html/openWB/ramdisk/smarthome_device_ret' + str(devicenumber), 'w')
json.dump(answer, f1)
f1.close()
