#!/usr/bin/env python3
from datetime import datetime, timezone
import os
import re
import requests
import sys
import traceback

Debug = int(os.environ.get('debug'))
myPid = str(os.getpid())

femskacopw = str(sys.argv[1])
femsip = str(sys.argv[2])


def DebugLog(message):
    local_time = datetime.now(timezone.utc).astimezone()
    print(local_time.strftime(format="%Y-%m-%d %H:%M:%S") + ": PID: " + myPid + ": " + message)


if Debug >= 2:
    DebugLog('Wechselrichter FEMS Passwort: ' + femskacopw)
    DebugLog('Wechselrichter FEMS IP: ' + femsip)

response = requests.get('http://'+femsip+':8084/rest/channel/_sum/ProductionActivePower', auth=("x", femskacopw)).json()
try:
    pvwatt = response["value"] * -1
except:
    traceback.print_exc()
    exit(1)

response = requests.get('http://'+femsip+':8084/rest/channel/_sum/ProductionActiveEnergy',
                        auth=("x", femskacopw)).json()
try:
    pvwh = response["value"]
except:
    traceback.print_exc()
    exit(1)

regex = '^-?[0-9]+$'
if re.search(regex, str(pvwatt)) == None:
    pvwatt = "0"
if re.search(regex, str(pvwh)) != None:
    if Debug >= 1:
        DebugLog('WR Energie: ' + str(pvwh))
    with open("/var/www/html/openWB/ramdisk/pvkwh", "w") as f:
        f.write(str(pvwh))
if Debug >= 1:
    DebugLog('WR Leistung: ' + str(pvwatt))
with open("/var/www/html/openWB/ramdisk/pvwatt", "w") as f:
    f.write(str(pvwatt))

exit(0)
