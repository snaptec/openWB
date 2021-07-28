#!/usr/bin/env python3

import json
import re
import requests
import sys

solarworld_emanagerip = str(sys.argv[1])

# Auslesen eines Solarworl eManagers über die integrierte JSON-API
response = requests.get('http://'+solarworld_emanagerip+'/rest/solarworld/lpvm/powerAndBatteryData', timeout=5)
emanagerantwort = json.loads(response)

em_in_watt = emanagerantwort["PowerIn"]
em_out_watt = emanagerantwort["PowerOut"]

# Bezug ist entweder -Out oder In; bei Einspeisung ist 'em_in_watt' immer 0
# use printf zum runden, LC_ALL=C wegen Dezimalpunkt
bezug_watt = int(em_in_watt - em_out_watt)

# wenn eManager aus bzw. keine Antwort ersetze leeren Wert durch eine 0
ra = '^-?[0-9]+$'

if re.search(bezug_watt, ra) == None:
    bezug_watt = "0"
with open("/var/www/html/openWB/ramdisk/wattbezug", "w") as f:
    f.write(str(bezug_watt))
