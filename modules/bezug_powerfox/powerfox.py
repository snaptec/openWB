#!/usr/bin/env python3
from datetime import datetime, timezone
import os
import requests
import sys
import traceback

powerfoxid = str(sys.argv[1])
powerfoxuser = str(sys.argv[2])
powerfoxpass = str(sys.argv[3])

Debug         = int(os.environ.get('debug'))
myPid         = str(os.getpid())

def DebugLog(message):
    local_time = datetime.now(timezone.utc).astimezone()
    print(local_time.strftime(format = "%Y-%m-%d %H:%M:%S") + ": PID: "+ myPid +": " + message)

if Debug >= 2:
    DebugLog('Powerfox ID: ' + powerfoxid)
    DebugLog('Powerfox User: ' + powerfoxuser)
    DebugLog('Powerfox Passwort: ' + powerfoxpass)

response = requests.get('https://backend.powerfox.energy/api/2.0/my/'+powerfoxid+'/current', auth=(powerfoxuser, powerfoxpass), timeout=3).json()
try:
    einspeisungwh = int(response['A_Minus'])
    with open("/var/www/html/openWB/ramdisk/einspeisungkwh", "w") as f:
        f.write(str(einspeisungwh))
except:
    traceback.print_exc()
    exit(1)
if Debug >= 1:
    DebugLog('Einspeisung: ' + str(einspeisungwh))

try:
    bezugwh = int(response['A_Plus'])
    with open("/var/www/html/openWB/ramdisk/bezugkwh", "w") as f:
        f.write(str(bezugwh))
except:
    traceback.print_exc()
    exit(1)
if Debug >= 1:
    DebugLog('Bezug: ' + str(bezugwh))

try:
    watt = int(response['Watt'])
    with open("/var/www/html/openWB/ramdisk/wattbezug", "w") as f:
        f.write(str(watt))
except:
    traceback.print_exc()
    exit(1)
if Debug >= 1:
    DebugLog('Watt: ' + str(watt))

exit(0)