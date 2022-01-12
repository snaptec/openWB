#!/usr/bin/env python3
from datetime import datetime, timezone
import os
import re
import requests
import sys
import traceback

Debug = int(os.environ.get('debug'))
myPid = str(os.getpid())

solarworld_emanagerip = str(sys.argv[1])


def DebugLog(message):
    local_time = datetime.now(timezone.utc).astimezone()
    print(local_time.strftime(format="%Y-%m-%d %H:%M:%S") + ": PID: " + myPid + ": " + message)


if Debug >= 2:
    DebugLog('PV Solarworld IP:' + solarworld_emanagerip)

# Auslesen eines Solarworld eManagers über die integrierte JSON-API
emanagerantwort = requests.get(
    "http://"+solarworld_emanagerip+"/rest/solarworld/lpvm/powerAndBatteryData", timeout=5).json()

try:
    wr_watt = int(emanagerantwort["PowerTotalPV"])
except:
    traceback.print_exc()
    exit(1)

# wenn eManager aus bzw. keine Antwort ersetze leeren Wert durch eine 0
ra = '^-?[0-9]+$'

if re.search(ra, str(wr_watt)) == None:
    wr_watt = 0

# PV ezeugte Leistung muss negativ sein
pvwatt = 0 - wr_watt
if Debug >= 1:
    DebugLog("PV-Leistung: "+str(pvwatt)+" W")
with open("/var/www/html/openWB/ramdisk/pvwatt", "w") as f:
    f.write(str(pvwatt))

exit(0)
