#!/usr/bin/python3
import sys
import json
import jq
import os
import requests

devicenumber = str(sys.argv[1])      
ipadr = os.environ.get('bezug_solarlog_ip') #IP-Adresse des SolarLog kommt vom PV Modul

# ID des Zählers im SolarLog (SolarLog base hat 2 RS485 Schnittstellen und die Sortierung scheint B/A zu schein)
# Daher am besten alle Werte mit folgendem cli commando abrufen und ggf mit der Webansicht http://ip/#ilang=DE&b=p_live_table abgleichen.
# curl --request POST --url http://<ip des Solarlogs>/getjp --header 'Content-Type: application/json' --data '{"782":null}'
# Die Zähler ID ist die Nummer vor dem Verbrauchswert.
smid = int(sys.argv[2])         

# Abfrage-URL, die das JSON liefert.
jsonurl = "http://"+str(ipadr)+"/getjp"

request_data_power = {'782':{str(smid):None}}
request_data_powerc = {'777': {'0':None}} # need more filtering
   
#json Key in dem der aktuelle Leistungswert stehen
jsonpower = '."782"."1"'               
# json enthält immer eine Liste von Tagen und alle Werte, letzer Array entry ist heute, Filter per Device ID
jsonpowerc = '."777"."0"[-1][1]['+str(smid)+']'

try:
    answer_power = json.loads(requests.post(jsonurl,json=request_data_power,timeout=3).content.decode('UTF-8'))
    power = jq.compile(jsonpower).input(answer_power).first()
    if (power==None):
        power=0
except:
    power = 0
    
try:
    answer_powerc = json.loads(requests.post(jsonurl,json=request_data_powerc,timeout=3).content.decode('UTF-8'))
    powerc = jq.compile(jsonpowerc).input(answer_powerc).first()
    if (powerc==None):
        powerc=0
except:
    powerc = 0

f1 = open('/var/www/html/openWB/ramdisk/smarthome_device_ret' + str(devicenumber), 'w')
answer = '{"power":' + str(power) + ',"powerc":' + str(powerc) + '}'
#print(answer)
json.dump(answer, f1)
f1.close()