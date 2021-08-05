#!/usr/bin/env python3

import re
import requests
import sys
import traceback

solarworld_emanagerip = str(sys.argv[1])

# Auslesen eines Solarworl eManagers über die integrierte JSON-API
emanagerantwort = requests.get('http://'+solarworld_emanagerip+'/rest/solarworld/lpvm/powerAndBatteryData', timeout=5).json()
try:
    em_in_watt = emanagerantwort["PowerIn"]
except:
    traceback.print_exc()
try:
    em_out_watt = emanagerantwort["PowerOut"]
except:
    traceback.print_exc()

# Bezug ist entweder -Out oder In; bei Einspeisung ist 'em_in_watt' immer 0
# use printf zum runden, LC_ALL=C wegen Dezimalpunkt
bezug_watt = int(em_in_watt - em_out_watt)

# wenn eManager aus bzw. keine Antwort ersetze leeren Wert durch eine 0
ra = '^-?[0-9]+$'

if re.search(bezug_watt, ra) == None:
    bezug_watt = "0"
with open("/var/www/html/openWB/ramdisk/wattbezug", "w") as f:
    f.write(str(bezug_watt))
