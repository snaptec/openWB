#!/usr/bin/env python3

from datetime import datetime, timezone
import os
import requests
import sys
import traceback

Debug = int(os.environ.get('debug'))
myPid = str(os.getpid())

discovergyuser = str(sys.argv[1])
discovergypass = str(sys.argv[2])
discovergypvid = str(sys.argv[3])

def DebugLog(message):
    local_time = datetime.now(timezone.utc).astimezone()
    print(local_time.strftime(format = "%Y-%m-%d %H:%M:%S") + ": PID: "+ myPid +": " + message)


if Debug >= 2:
    DebugLog('Wechselrichter Discovergy User: ' + discovergyuser)
    DebugLog('Wechselrichter Discovergy Passwort: ' + discovergypass)
    DebugLog('Wechselrichter Discovergy ID: ' + discovergypvid)

params = (
    ('meterId', discovergypvid),
)
output = requests.get('https://api.discovergy.com/public/v1/last_reading', params=params, auth=(discovergyuser, discovergypass), timeout=5).json()
try:
    pvwh = output["values"]["energyOut"]
except:
    traceback.print_exc()
    exit(1)
pvwh = pvwh / 10000000
if Debug >= 1:
    DebugLog('WR Energie: ' + str(pvwh))
with open("/var/www/html/openWB/ramdisk/pvkwh", "w") as f:
    f.write(str(pvwh))

try:
    watt = output["values"]["power"]
except:
    traceback.print_exc()
    exit(1)
watt = watt / 1000
if Debug >= 1:
    DebugLog('WR Leistung: ' + str(watt))
with open("/var/www/html/openWB/ramdisk/pvwatt", "w") as f:
    f.write(str(watt))

exit(0)
