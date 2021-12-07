#!/usr/bin/env python3
from datetime import datetime, timezone
import os
import datetime
import requests
import sys
import traceback

solarwattmethod = int(sys.argv[1])
speicher1_ip = str(sys.argv[2])
speicher1_ip2 = str(sys.argv[3])

Debug = int(os.environ.get('debug'))
myPid = str(os.getpid())


def DebugLog(message):
    local_time = datetime.now(timezone.utc).astimezone()
    print(local_time.strftime(format="%Y-%m-%d %H:%M:%S") + ": PID: " + myPid + ": " + message)


if Debug >= 2:
    DebugLog('Solarwatt Methode: ' + str(solarwattmethod))
    DebugLog('Solarwatt IP1: ' + speicher1_ip)
    DebugLog('Solarwatt IP2: ' + speicher1_ip2)


if solarwattmethod == 0:  # Abruf über Energy Manager
    sresponse = requests.get('http://'+speicher1_ip+'/rest/kiwigrid/wizard/devices', timeout=3).json()
    if len(str(sresponse)) < 10:
        with open("/var/www/html/openWB/ramdisk/wattbezug", "r") as f:
            bezugwatt = f.read()
    else:
        for item in sresponse["result"]["items"].values():
            try:
                bezugw = int(item["tagValues"]["PowerConsumedFromGrid"]["value"])
            except KeyError:
                pass

        for item in sresponse["result"]["items"].values():
            try:
                einspeisungw = int(sresponse["result"]["items"][item]["tagValues"]["PowerOut"]["value"])
            except KeyError:
                pass
        bezugwatt = bezugw - einspeisungw
if solarwattmethod == 1:  # Abruf über Gateway
    sresponse = requests.get('http://'+speicher1_ip2+':8080/', timeout=3).json()
    bezugwatt = int(sresponse["FData"]["PGrid"])

if Debug >= 1:
    DebugLog("Netzbezug: "+str(bezugwatt)+" W")
with open("/var/www/html/openWB/ramdisk/wattbezug", "w") as f:
    f.write(str(bezugwatt))

exit(0)
