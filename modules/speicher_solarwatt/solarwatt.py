#!/usr/bin/env python3

from datetime import datetime, timezone
import os
import requests
import sys
import traceback

from requests.api import get

Debug = int(os.environ.get('debug'))
myPid = str(os.getpid())

solarwattmethod = str(sys.argv[1])
speicher1_ip = str(sys.argv[2])
speicher1_ip2 = str(sys.argv[3])


def DebugLog(message):
    local_time = datetime.now(timezone.utc).astimezone()
    print(local_time.strftime(format="%Y-%m-%d %H:%M:%S") + ": PID: " + myPid + ": " + message)


if Debug >= 2:
    DebugLog('Speicher Methode: ' + solarwattmethod)
    DebugLog('Speicher IP1: ' + speicher1_ip)
    DebugLog('Speicher IP2: ' + speicher1_ip2)


def get_value(key, sresponse):
    value = 0
    try:
        for item in sresponse["result"]["items"]:
            if "tagValues" in sresponse["result"]["items"][item]:
                if key in sresponse["result"]["items"][item]["tagValues"]:
                    if "value" in sresponse["result"]["items"][item]["tagValues"][key]:
                        value = int(sresponse["result"]["items"][item]["tagValues"][key]["value"])
                        break
    except:
        traceback.print_exc()
        exit(1)
    return value


if solarwattmethod == 0:  # Abruf über Energy Manager
    sresponse = requests.get('http://'+speicher1_ip+'/rest/kiwigrid/wizard/devices', timeout=5).json()
    if len(str(sresponse)) < 10:
        sys.exit(1)

    speichere = get_value("PowerConsumedFromStorage", sresponse)
    speicherein = get_value("PowerOutFromStorage", sresponse)
    speicheri = get_value("PowerBuffered", sresponse)
    speicherleistung = int((speichere + speicherein - speicheri) * -1)
    speichersoc = get_value("StateOfCharge", sresponse)


elif solarwattmethod == 1:  # Abruf über Gateway
    sresponse = requests.get('http://'+speicher1_ip2+':8080/', timeout=3).json()
    if len(str(sresponse)) < 10:
        sys.exit(1)
    ibat = sresponse["FData"]["IBat"]
    vbat = sresponse["FData"]["VBat"]

    speicherleistung = ibat * vbat
    speicherleistung = int(speicherleistung / (-1))
    speichersoc = int(sresponse["SData"]["SoC"])
    if Debug >= 1:
        DebugLog('SpeicherSoC: ' + str(speichersoc))
    if not str(speichersoc).isnumeric():
        DebugLog('SpeicherSoc nicht numerisch. -->0')
        speichersoc = 0
else:
    raise Exception("Unbekannte Abrufmethode fuer Solarwatt")

DebugLog("Speicherleistung: "+str(speicherleistung)+" W")
with open("/var/www/html/openWB/ramdisk/speicherleistung", "w") as f:
    f.write(str(speicherleistung))
DebugLog("SpeicherSoC: "+str(speichersoc)+" %")
with open("/var/www/html/openWB/ramdisk/speichersoc", "w") as f:
    f.write(str(speichersoc))

exit(0)
