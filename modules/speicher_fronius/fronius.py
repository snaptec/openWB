#!/usr/bin/env python3

from datetime import datetime, timezone
import os
import re
import requests
import sys
import traceback

Debug = int(os.environ.get('debug'))
myPid = str(os.getpid())

wrfroniusip = str(sys.argv[1])
wrfroniusisgen24 = int(sys.argv[2])
froniuserzeugung = sys.argv[3]


def DebugLog(message):
    local_time = datetime.now(timezone.utc).astimezone()
    print(local_time.strftime(format="%Y-%m-%d %H:%M:%S") + ": PID: " + myPid + ": " + message)


if Debug >= 2:
    DebugLog('Speicher IP: ' + wrfroniusip)

# Auslesen eines Fronius Symo WR Hybrid mit Fronius Smartmeter und Batterie über die integrierte JSON-API des WR.
params = (
    ('Scope', 'System'),
)
response = requests.get('http://'+wrfroniusip+'/solar_api/v1/GetPowerFlowRealtimeData.fcgi',
                        params=params, timeout=5).json()
try:
    speicherwatt = int(response["Body"]["Data"]["Site"]["P_Akku"])
except:
    traceback.print_exc()
    exit(1)
speicherwatt = speicherwatt * -1

# wenn WR aus bzw. im standby (keine Antwort) ersetze leeren Wert durch eine 0
ra = '^-?[0-9]+$'
if re.search(ra, str(speicherwatt)) == None:
    speicherwatt = "0"
if Debug >= 1:
    DebugLog('Speicherleistung: ' + str(speicherwatt))
with open("/var/www/html/openWB/ramdisk/speicherleistung", "w") as f:
    f.write(str(speicherwatt))

try:
    if wrfroniusisgen24 == 1:
        response_soc = requests.get('http://'+wrfroniusip+'/solar_api/v1/GetStorageRealtimeData.cgi', timeout=5).json()
        speichersoc = int(response["Body"]["Data"][froniuserzeugung]["Controller"]["StateOfCharge_Relative"])
    else:
        speichersoc = int(response["Body"]["Data"]["Inverters"]["1"]["SOC"])
except:
    traceback.print_exc()
    exit(1)
if re.search(ra, str(speichersoc)) == None:
    speichersoc = "0"
if Debug >= 1:
    DebugLog('Soc: ' + str(speichersoc))
with open("/var/www/html/openWB/ramdisk/speichersoc", "w") as f:
    f.write(str(speichersoc))

exit(0)
