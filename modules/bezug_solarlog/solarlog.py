#!/usr/bin/env python3
from datetime import datetime, timezone
import os
import json
import requests
import sys
import traceback

bezug_solarlog_ip = str(sys.argv[1])
bezug_solarlog_speicherv = str(sys.argv[2])

Debug         = int(os.environ.get('debug'))
myPid         = str(os.getpid())

def DebugLog(message):
    local_time = datetime.now(timezone.utc).astimezone()
    print(local_time.strftime(format = "%Y-%m-%d %H:%M:%S") + ": PID: "+ myPid +": " + message)

if Debug >= 2:
    DebugLog('Solarlog IP: ' + bezug_solarlog_ip)
    DebugLog('Solarlog Speicher: ' + bezug_solarlog_speicherv)

data = {"801": {"170": None}}
data = json.dumps(data)
response = requests.post('http://'+bezug_solarlog_ip+'/getjp', data=data, timeout=5).json()

try:
    pvwatt = response["801"]["170"]["101"]
except:
    traceback.print_exc()
    exit(1)
try:
    hausverbrauch = response["801"]["170"]["110"]
except:
    traceback.print_exc()
    exit(1)
bezugwatt = hausverbrauch - pvwatt
try:
    pvkwh = response["801"]["170"]["109"]
except:
    traceback.print_exc()
    exit(1)

if bezug_solarlog_speicherv == 1:
    with open("ramdisk/speicherleistung", "r") as f:
        speicherleistung = f.read()
    bezugwatt = bezugwatt + speicherleistung
if pvwatt > 5:
    pvwatt = pvwatt*-1

if Debug >= 1:
    DebugLog('Leistung: ' + str(bezugwatt))
with open("/var/www/html/openWB/ramdisk/wattbezug", "w") as f:
    f.write(str(bezugwatt))
if Debug >= 1:
    DebugLog('PV Leistung: ' + str(pvwatt))
with open("/var/www/html/openWB/ramdisk/pvwatt", "w") as f:
    f.write(str(pvwatt))
if Debug >= 1:
    DebugLog('PV Energie: ' + str(pvkwh))
with open("/var/www/html/openWB/ramdisk/pvkwh", "w") as f:
    f.write(str(pvkwh))
pvkwhk = pvkwh*1000
with open("/var/www/html/openWB/ramdisk/pvkwhk", "w") as f:
    f.write(str(pvkwhk))

exit(0)