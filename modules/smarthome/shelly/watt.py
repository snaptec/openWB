#!/usr/bin/python3
import sys
import os
import time
import json
import getopt
import socket
import struct
import codecs
import binascii
import urllib.request

def totalPowerFromShellyJson(json):
    if 'meters' in answer:
        meters = answer['meters'] # shelly
    else:
        meters = answer['emeters'] # shellyEM & shelly3EM
    total = 0
    # shellyEM has one meter, shelly3EM has three meters:
    for meter in meters:
        total = total + meter['power']
    return int(total)

named_tuple = time.localtime() # getstruct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S shelly watty.py", named_tuple)
devicenumber=str(sys.argv[1])
ipadr=str(sys.argv[2])
uberschuss=int(sys.argv[3])
answer = json.loads(str(urllib.request.urlopen("http://"+str(ipadr)+"/status", timeout=3).read().decode("utf-8")))
aktpower = totalPowerFromShellyJson(answer)
relais = int(answer['relays'][0]['ison'])
powerc = 0
answer = '{"power":' + str(aktpower) + ',"powerc":' + str(powerc) + ',"on":' + str(relais) + '} '
f1 = open('/var/www/html/openWB/ramdisk/smarthome_device_ret' + str(devicenumber), 'w')
json.dump(answer,f1)
f1.close()
