#!/usr/bin/env python3

import re
import requests
import sys

wrfroniusip = str(sys.argv[1])

# Auslesen eines Fronius Symo WR Hybrid mit Fronius Smartmeter und Batterie über die integrierte JSON-API des WR.
params = (
    ('Scope', 'System'),
)
response = requests.get('http://'+wrfroniusip+'/solar_api/v1/GetPowerFlowRealtimeData.fcgi', params=params, timeout=5).json()
speicherwatt = int(response["Body"]["Data"]["Site"]["P_Akku"])
speicherwatt = speicherwatt * -1

# wenn WR aus bzw. im standby (keine Antwort) ersetze leeren Wert durch eine 0
ra = '^-?[0-9]+$'
if re.search(ra, speicherwatt) == None:
    speicherwatt = "0"
with open("/var/www/html/openWB/ramdisk/speicherleistung", "w") as f:
    f.write(str(speicherwatt))

speichersoc = int(response["Body"]["Data"]["Inverters"]["1"]["SOC"])
if re.search(ra, speichersoc) == None:
    speichersoc = "0"
with open("/var/www/html/openWB/ramdisk/speichersoc", "w") as f:
    f.write(str(speichersoc))
