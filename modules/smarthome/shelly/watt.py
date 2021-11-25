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
gen = '1'

# test dic
g_dictionary = {"gen": 1}

a_dictionary = {"switch:0":{"id": 0, "source": "init", "output": True, "apower": 55.000, "voltage": 218.794,"aenergy": {"total":4327.45,"minute_ts":1637430901},"temperature":{"tC":49.1, "tF":120.3}}}

# test dic ende
# lesen endpoint, gen bestimmem. gen 1 hat unter Umstaenden keinen Eintrag
fname =   '/var/www/html/openWB/ramdisk/smarthome_device_ret' + str(devicenumber) + '_shelly_info'
fnameg =   '/var/www/html/openWB/ramdisk/smarthome_device_ret' + str(devicenumber) + '_shelly_infog'
if os.path.isfile(fnameg):
    f = open(fnameg, 'r')
    gen=str(f.read())
    f.close()
else:   
    answergen= json.loads(str(urllib.request.urlopen("http://"+str(ipadr)+"/shelly", timeout=3).read().decode("utf-8")))
    #answergen.update(g_dictionary)
    f = open(fname, 'w')
    json.dump(answergen,f)
    f.close()
    if 'gen' in answergen:
        gen = str(int(answergen['gen']))
    f = open(fnameg, 'w')
    f.write(str(gen))
    f.close()
# Versuche Daten von Shelly abzurufen.
try:
    if (gen == "1"):
        answer = json.loads(str(urllib.request.urlopen("http://"+str(ipadr)+"/status", timeout=3).read().decode("utf-8")))
        #answer.update(a_dictionary)  
        # fake new gen
        #gen = '2'
    else:
        answer = json.loads(str(urllib.request.urlopen("http://"+str(ipadr)+"/rpc/Shelly.GetStatus", timeout=3).read().decode("utf-8")))
    f = open('/var/www/html/openWB/ramdisk/smarthome_device_ret' + str(devicenumber) + '_shelly', 'w')
    f.write(str(answer))
    f.close()
except:
    print("failed to connect to device on " +  ipadr + ", setting all values to 0")
#answer.update(a_dictionary)
# Versuche Werte aus der Antwort zu extrahieren.
try:
    if (gen == "1"):
        aktpower = totalPowerFromShellyJson(answer)
    else:
        aktpower = int(answer['switch:0'] ['apower'])
except:
    pass

try:
    if (gen == "1"):
        relais = int(answer['relays'][0]['ison'])
    else:
        relais = int(answer['switch:0'] ['output'])
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
