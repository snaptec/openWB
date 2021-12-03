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
        for item in sresponse["result"]["items"]:
            try:
                if "tagValues" in sresponse["result"]["items"][item]:
                    if "PowerConsumedFromGrid" in sresponse["result"]["items"][item]["tagValues"]:
                        if "value" in sresponse["result"]["items"][item]["tagValues"]["PowerConsumedFromGrid"]:
                            bezugw = int(sresponse["result"]["items"][item]["tagValues"]
                                         ["PowerConsumedFromGrid"]["value"])
                            break
            except:
                traceback.print_exc()
                exit(1)
        for item in sresponse["result"]["items"]:
            try:
                if "tagValues" in sresponse["result"]["items"][item]:
                    if "PowerOut" in sresponse["result"]["items"][item]["tagValues"]:
                        if "value" in sresponse["result"]["items"][item]["tagValues"]["PowerOut"]:
                            einspeisungw = int(sresponse["result"]["items"][item]["tagValues"]["PowerOut"]["value"])
                            break
            except:
                traceback.print_exc()
                exit(1)
        bezugwatt = int(bezugw - einspeisungw)
if solarwattmethod == 1:  # Abruf über Gateway
    sresponse = requests.get('http://'+speicher1_ip2+':8080/', timeout=3).json()
    if len(str(sresponse)) < 10:
        with open("/var/www/html/openWB/ramdisk/wattbezug", "r") as f:
            bezugwatt = f.read()
    else:
        try:
            bezugwatt = int(sresponse["FData"]["PGrid"])
        except:
            traceback.print_exc()
            exit(1)

if Debug >= 1:
    DebugLog("Netzbezug: "+str(bezugwatt)+" W")
with open("/var/www/html/openWB/ramdisk/wattbezug", "w") as f:
    f.write(str(bezugwatt))

exit(0)
