#!/usr/bin/env python3

from datetime import datetime, timezone
import os
import re
import requests
import sys
import traceback

Debug = int(os.environ.get("debug"))
myPid = str(os.getpid())

multifems = str(sys.argv[1])
femskacopw = str(sys.argv[2])
femsip = str(sys.argv[3])


def DebugLog(message):
    local_time = datetime.now(timezone.utc).astimezone()
    print(local_time.strftime(format="%Y-%m-%d %H:%M:%S") + ": PID: " + myPid + ": " + message)


if Debug >= 2:
    DebugLog("Speicher IP: " + femsip)
    DebugLog("Speicher Passwort: " + femskacopw)
    DebugLog("Speicher Multi: " + multifems)


def write_ramdisk(value, file):
    try:
        if file == "speichersoc":
            if re.search("^[-+]?[0-9]+.?[0-9]*$", str(value)) == None:
                value = "0"
        if Debug >= 1:
            DebugLog(file+': ' + str(value))
        with open("/var/www/html/openWB/ramdisk/"+file, "w") as f:
            f.write(str(value))
    except:
        traceback.print_exc()
        exit(1)


if multifems == "0":
    try:
        response = requests.get(
            "http://" + femsip + ":8084/rest/channel/ess0/(Soc|ActiveChargeEnergy|ActiveDischargeEnergy)",
            auth=("x", femskacopw)).json()
    except:
        traceback.print_exc()
        exit(1)
    for singleValue in response:
        address = singleValue["address"]
        if (address == "ess0/Soc"):
            write_ramdisk(singleValue["value"], "speichersoc")
        elif address == "ess0/ActiveChargeEnergy":
            write_ramdisk(singleValue["value"], "speicherikwh")
        elif address == "ess0/ActiveDischargeEnergy":
            write_ramdisk(singleValue["value"], "speicherekwh")
else:
    try:
        response = requests.get(
            "http://" + femsip + ":8084/rest/channel/ess2/(Soc|ActiveChargeEnergy|ActiveDischargeEnergy)",
            auth=("x", femskacopw)).json()
    except:
        traceback.print_exc()
        exit(1)
    for singleValue in response:
        address = singleValue["address"]
        if (address == "ess2/Soc"):
            write_ramdisk(singleValue["value"], "speichersoc")
        elif address == "ess2/ActiveChargeEnergy":
            write_ramdisk(singleValue["value"], "speicherikwh")
        elif address == "ess2/ActiveDischargeEnergy":
            write_ramdisk(singleValue["value"], "speicherekwh")

try:
    response = requests.get(
        "http://" + femsip + ":8084/rest/channel/_sum/(GridActivePower|ProductionActivePower|ConsumptionActivePower)",
        auth=("x", femskacopw)).json()
except:
    traceback.print_exc()
    exit(1)
for singleValue in response:
    address = singleValue["address"]
    if (address == "_sum/GridActivePower"):
        grid = singleValue["value"]
    elif address == "_sum/ProductionActivePower":
        pv = singleValue["value"]
    elif address == "_sum/ConsumptionActivePower":
        haus = singleValue["value"]

leistung = grid + pv - haus

ra = "^[-+]?[0-9]+.?[0-9]*$"
if re.search(ra, str(leistung)) == None:
    leistung = "0"
if Debug >= 1:
    DebugLog('Speicherleistung: ' + str(leistung))
with open("/var/www/html/openWB/ramdisk/speicherleistung", "w") as f:
    f.write(str(leistung))

exit(0)
