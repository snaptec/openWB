#!/usr/bin/env python3
from datetime import datetime, timezone
import os
import requests
import sys
import traceback

Debug = int(os.environ.get('debug'))
myPid = str(os.getpid())

speicher1_ip = str(sys.argv[1])


def DebugLog(message):
    local_time = datetime.now(timezone.utc).astimezone()
    print(local_time.strftime(format="%Y-%m-%d %H:%M:%S") + ": PID: " + myPid + ": " + message)


if Debug >= 2:
    DebugLog('PV Solarwatt IP:' + speicher1_ip)


sresponse = requests.get('http://'+speicher1_ip+'/rest/kiwigrid/wizard/devices', timeout=3).json()

try:
    for item in sresponse["result"]["items"]:
        if "tagValues" in sresponse["result"]["items"][item]:
            if "PowerProduced" in sresponse["result"]["items"][item]["tagValues"]:
                if "value" in sresponse["result"]["items"][item]["tagValues"]["PowerProduced"]:
                    pvwatt = int(sresponse["result"]["items"][item]["tagValues"]["PowerProduced"]["value"])
                    break
except:
    traceback.print_exc()
    exit(1)
pvwatt = pvwatt * -1
if Debug >= 1:
    DebugLog("PV-Leistung: "+str(pvwatt)+" W")
with open("/var/www/html/openWB/ramdisk/pvwatt", "w") as f:
    f.write(str(pvwatt))

exit(0)
