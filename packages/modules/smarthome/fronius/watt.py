#!/usr/bin/python3
import sys
import json
import jq
import urllib.request

devicenumber = str(sys.argv[1])
ipadr = str(sys.argv[2])  # IP-ADresse des Fronius Wechselrichters, mit dem der Zähler kommuniziert
smid = int(sys.argv[3])  # ID des Zählers im Wechselrichter (Hauptzähler 0, weitere fortlaufend)

# Abfrage-URL, die die .json Antwort liefert.
jsonurl = "http://"+str(ipadr)+"/solar_api/v1/GetMeterRealtimeData.cgi?Scope=Device&DeviceId="+str(smid)
jsonpower = ".Body.Data.PowerReal_P_Sum"  # json Key in dem der aktuelle Leistungswert steht
jsonpowerc = ".Body.Data.EnergyReal_WAC_Sum_Consumed"  # json Key in dem der summierte Verbrauch steht

answer = json.loads(str(urllib.request.urlopen(jsonurl, timeout=3).read().decode("utf-8")))

try:
    power = jq.compile(jsonpower).input(answer).first()
    power = int(abs(power))
except Exception:
    power = 0

try:
    powerc = jq.compile(jsonpowerc).input(answer).first()
    powerc = int(abs(powerc))
except Exception:
    powerc = 0

f1 = open('/var/www/html/openWB/ramdisk/smarthome_device_ret' + str(devicenumber), 'w')
answer = '{"power":' + str(power) + ',"powerc":' + str(powerc) + '}'
json.dump(answer, f1)
f1.close()
