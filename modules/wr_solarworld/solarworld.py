#!/usr/bin/env python3

import re
import requests
import sys

solarworld_emanagerip = str(sys.argv[1])

# Auslesen eines Solarworld eManagers über die integrierte JSON-API
emanagerantwort = requests.get(solarworld_emanagerip+"/rest/solarworld/lpvm/powerAndBatteryData", timeout=5)
emanagerantwort = emanagerantwort.json()

wr_watt = int(emanagerantwort["PowerTotalPV"])

# wenn eManager aus bzw. keine Antwort ersetze leeren Wert durch eine 0
ra = '^-?[0-9]+$'

if re.search(ra, wr_watt) == None:
    wr_watt = "0"

# PV ezeugte Leistung muss negativ sein
pvwatt = 0 - wr_watt
with open("/var/www/html/openWB/ramdisk/pvwatt", "w") as f:
    f.write(str(pvwatt))
