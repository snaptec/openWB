#!/usr/bin/env python3

import datetime
import requests
import sys

from requests.api import get

base_dir = str(sys.argv[1])
debug = str(sys.argv[2])
solarwattmethod = str(sys.argv[3])
speicher1_ip = str(sys.argv[4])
speicher1_ip2 = str(sys.argv[5])

ramdisk_dir = base_dir+"/ramdisk"
module = "Speicher"
logfile = ramdisk_dir+"/openWB.log"


def debugLog(msg):
    if debug > 0:
        timestamp = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        with open(logfile, "a") as f:
            f.write(str(timestamp)+": "+str(module)+": "+msg)


def get_value(key, sresponse):
    value = None
    for item in sresponse["result"]["items"]:
        if "tagValues" in sresponse["result"]["items"][item]:
            if key in sresponse["result"]["items"][item]["tagValues"]:
                if "value" in sresponse["result"]["items"][item]["tagValues"][key]:
                    value = int(sresponse["result"]["items"][item]["tagValues"][key]["value"])
                    break
    return value


if solarwattmethod == 0:  # Abruf über Energy Manager
    sresponse = requests.get('http://'+speicher1_ip+'/rest/kiwigrid/wizard/devices', timeout=5).json()
    if len(str(sresponse)) < 10:
        sys.exit(1)
    
    speichere=get_value("PowerConsumedFromStorage", sresponse)
    speicherein=get_value("PowerOutFromStorage", sresponse)
    speicheri=get_value("PowerBuffered", sresponse)
    speicherleistung=int((speichere + speicherin - speicheri) *-1)
    speichersoc=get_value("StateOfCharge", sresponse)


if solarwattmethod == 1: 	#Abruf über Gateway
    sresponse=requests.get('http://'+speicher1_ip2+':8080/', timeout=3).json()
    if len(str(sresponse)) < 10:
        sys.exit(1)
    
    ibat=sresponse["FData"]["IBat"]
    vbat=sresponse["FData"]["VBat"]
    speicherleistung=ibat * vbat
    speicherleistung=int(speicherleistung / (-1))
    speichersoc=int(sresponse["SData"]["SoC"])


debugLog("Speicherleistung: "+speicherleistung+" W")
with open("/var/www/html/openWB/ramdisk/speicherleistung", "w") as f:
    f.write(str(speicherleistung))
debugLog("SpeicherSoC: "+speichersoc+" %")
with open("/var/www/html/openWB/ramdisk/speichersoc", "w") as f:
    f.write(str(speichersoc))
