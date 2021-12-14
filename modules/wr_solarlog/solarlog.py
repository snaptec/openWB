#!/usr/bin/env python3

from datetime import datetime, timezone
import os
import json
import requests
import sys
import traceback

Debug = int(os.environ.get('debug'))
myPid = str(os.getpid())

bezug_solarlog_ip = str(sys.argv[1])

def DebugLog(message):
    local_time = datetime.now(timezone.utc).astimezone()
    print(local_time.strftime(format = "%Y-%m-%d %H:%M:%S") + ": PID: "+ myPid +": " + message)


if Debug >= 2:
    DebugLog('Wechselrichter Solarlog IP: ' + bezug_solarlog_ip)

data = {"801": {"170": None}}
data = json.dumps(data)
response = requests.post("http://"+bezug_solarlog_ip+'/getjp', data=data, timeout=5).json()
try:
    pvwatt = response["801"]["170"]["101"]
except:
    traceback.print_exc()
    exit(1)
try:
    pvkwh = response["801"]["170"]["109"]
except:
    traceback.print_exc()
    exit(1)

if pvwatt > 5:
    pvwatt = pvwatt*-1

if Debug >= 1:
    DebugLog('WR Leistung: ' + str(pvwatt))
with open("/var/www/html/openWB/ramdisk/pvwatt", "w") as f:
    f.write(str(pvwatt))
if Debug >= 1:
    DebugLog('WR Energie: ' + str(pvkwh))
with open("/var/www/html/openWB/ramdisk/pvkwh", "w") as f:
    f.write(str(pvkwh))

exit(0)