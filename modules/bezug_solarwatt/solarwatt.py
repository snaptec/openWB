#!/usr/bin/env python3

import datetime
import requests
import sys
import traceback

base_dir = str(sys.argv[1])
debug = str(sys.argv[2])
solarwattmethod = str(sys.argv[3])
speicher1_ip = str(sys.argv[4])
speicher1_ip2 = str(sys.argv[5])

ramdisk_dir = base_dir+"/ramdisk"
module = "EVU"
logfile = ramdisk_dir+"/openWB.log"
Debug = debug
bezug_file = ramdisk_dir+"/wattbezug"


def debugLog(msg):
    if Debug > 0:
        timestamp = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        with open(logfile, "a") as f:
            f.write(str(timestamp)+": "+str(module)+": "+msg)


if solarwattmethod == 0:  # Abruf über Energy Manager
    sresponse = requests.get('http://'+speicher1_ip+'/rest/kiwigrid/wizard/devices', timeout=3).json()
    if len(str(sresponse)) < 10:
        with open(bezug_file, "r") as f:
            bezugwatt = f.read()
    else:
        for item in sresponse["result"]["items"]:
            try:
                if "tagValues" in sresponse["result"]["items"][item]:
                    if "PowerConsumedFromGrid" in sresponse["result"]["items"][item]["tagValues"]:
                        if "value" in sresponse["result"]["items"][item]["tagValues"]["PowerConsumedFromGrid"]:
                            bezugw = int(sresponse["result"]["items"][item]["tagValues"]["PowerConsumedFromGrid"]["value"])
            except:
                traceback.print_exc()
        einspeisungw =$(echo $sresponse | jq '.result.items | .[] | select(.tagValues.PowerOut.value != null) | .tagValues.PowerOut.value' | head - n 1 | sed 's/\..*$//')
        for item in sresponse["result"]["items"]:
            try:
                if "tagValues" in sresponse["result"]["items"][item]:
                    if "PowerOut" in sresponse["result"]["items"][item]["tagValues"]:
                        if "value" in sresponse["result"]["items"][item]["tagValues"]["PowerOut"]:
                            bezugw = int(sresponse["result"]["items"][item]["tagValues"]["PowerOut"]["value"])
            except:
                traceback.print_exc()
        bezugwatt = int(bezugw - einspeisungw)
if solarwattmethod == 1:  # Abruf über Gateway
    sresponse = requests.get('http://'+speicher1_ip2+':8080/', timeout=3).json()
    if len(str(sresponse)) < 10:
        with open(bezug_file, "r") as f:
            bezugwatt = f.read()
    else:
        try:
            bezugwatt = int(sresponse["FData"]["PGrid"])
        except:
            traceback.print_exc()

debugLog("Netzbezug: "+str(bezugwatt)+" W")
with open(bezug_file, "w") as f:
    f.write(str(bezugwatt))
