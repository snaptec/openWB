#!/usr/bin/env python3

import datetime
import requests
import sys

base_dir = str(sys.argv[1])
debug = str(sys.argv[2])
speicher1_ip = str(sys.argv[3])

ramdisk_dir = base_dir+"/ramdisk"
module = "PV"
logfile = ramdisk_dir+"/openWB.log"


def debugLog(msg):
    if debug > 0:
        timestamp = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        with open(logfile, "a") as f:
            f.write(str(timestamp)+": "+str(module)+": "+msg)


sresponse = requests.get('http://'+speicher1_ip+'/rest/kiwigrid/wizard/devices', timeout=3)
sresponse = sresponse.json()

for item in sresponse["result"]["items"]:
    if "tagValues" in sresponse["result"]["items"][item]:
        if "PowerProduced" in sresponse["result"]["items"][item]["tagValues"]:
            if "value" in sresponse["result"]["items"][item]["tagValues"]["PowerProduced"]:
                pvwatt = int(sresponse["result"]["items"][item]["tagValues"]["PowerProduced"]["value"])
                break
debugLog("PV-Leistung: "+str(pvwatt)+" W")
pvwatt = pvwatt * -1

with open("/var/www/html/openWB/ramdisk/pvwatt", "w") as f:
    f.write(str(pvwatt))
