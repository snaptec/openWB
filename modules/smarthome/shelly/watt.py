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

def totalPowerFromShellyJson(answer):
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

# Setze Default-Werte, andernfalls wird der letzte Wert ewig fortgeschrieben. Insbesondere wichtig für aktuelle Leistung
powerc = 0 # Zähler wird beim Neustart auf 0 gesetzt, darf daher nicht übergeben werden.
temp0 = '0.0'
temp1 = '0.0'
temp2 = '0.0'
aktpower = 0
relais = 0

# Versuche Daten von Shelly abzurufen.
try:
    answer = json.loads(str(urllib.request.urlopen("http://"+str(ipadr)+"/status", timeout=3).read().decode("utf-8")))
    f = open('/var/www/html/openWB/ramdisk/smarthome_device_ret' + str(devicenumber) + '_shelly', 'w')
    f.write(str(answer))
    f.close()
except:
    print("failed to connect to device on " +  ipadr + ", setting all values to 0")

# Versuche Werte aus der Antwort zu extrahieren.
try:
    aktpower = totalPowerFromShellyJson(answer)
except:
    pass

try:
    relais = int(answer['relays'][0]['ison'])
except:
    pass

try:
    temp0 = str(answer['ext_temperature']['0']['tC'])
except:
    pass

try:
    temp1 = str(answer['ext_temperature']['1']['tC'])
except:
    pass

try:
    temp2 = str(answer['ext_temperature']['2']['tC'])
except:
    pass

answer = '{"power":' + str(aktpower) + ',"powerc":' + str(powerc) + ',"on":' + str(relais) + ',"temp0":' + str(temp0) + ',"temp1":' + str(temp1) + ',"temp2":' + str(temp2) + '} '

f1 = open('/var/www/html/openWB/ramdisk/smarthome_device_ret' + str(devicenumber), 'w')
json.dump(answer,f1)
f1.close()
