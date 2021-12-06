#!/usr/bin/env python3
from datetime import datetime, timezone
import os
import re
import requests
import sys
import traceback

solarworld_emanagerip = str(sys.argv[1])

Debug = int(os.environ.get('debug'))
myPid = str(os.getpid())


def DebugLog(message):
    local_time = datetime.now(timezone.utc).astimezone()
    print(local_time.strftime(format="%Y-%m-%d %H:%M:%S") + ": PID: " + myPid + ": " + message)


if Debug >= 2:
    DebugLog('Solarworld IP: ' + solarworld_emanagerip)

# Auslesen eines Solarworl eManagers über die integrierte JSON-API
emanagerantwort = requests.get(
    'http://'+solarworld_emanagerip+'/rest/solarworld/lpvm/powerAndBatteryData', timeout=5).json()
try:
    em_in_watt = emanagerantwort["PowerIn"]
except:
    traceback.print_exc()
    exit(1)
try:
    em_out_watt = emanagerantwort["PowerOut"]
except:
    traceback.print_exc()
    exit(1)

# Bezug ist entweder -Out oder In; bei Einspeisung ist 'em_in_watt' immer 0
bezug_watt = int(em_in_watt - em_out_watt)

# wenn eManager aus bzw. keine Antwort ersetze leeren Wert durch eine 0
ra = '^-?[0-9]+$'

if Debug >= 1:
    DebugLog('Leistung: ' + str(bezug_watt))
with open("/var/www/html/openWB/ramdisk/wattbezug", "w") as f:
    f.write(str(bezug_watt))

exit(0)
