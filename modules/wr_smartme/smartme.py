#!/usr/bin/env python3
from datetime import datetime, timezone
import os
import re
import requests
import sys
import traceback

Debug = int(os.environ.get('debug'))
myPid = str(os.getpid())

wr_smartme_url = str(sys.argv[1])
wr_smartme_user = str(sys.argv[2])
wr_smartme_pass = str(sys.argv[3])

def DebugLog(message):
    local_time = datetime.now(timezone.utc).astimezone()
    print(local_time.strftime(format = "%Y-%m-%d %H:%M:%S") + ": PID: "+ myPid +": " + message)


if Debug >= 2:
    DebugLog('Wechselrichter smartme URL: ' + wr_smartme_url)
    DebugLog('Wechselrichter smartme User: ' + wr_smartme_user)
    DebugLog('Wechselrichter smartme Passwort: ' + wr_smartme_pass)

# Daten einlesen
response = requests.get(wr_smartme_url, auth=(wr_smartme_user, wr_smartme_pass), timeout=10).json()
# Aktuelle Leistung (kW --> W)
try:
    wattwr = response["ActivePower"]
    wattwr = round(wattwr * 1000, 3)
    wattwr = int(wattwr)
except:
    traceback.print_exc()
    exit(1)

# Zählerstand Export (kWh --> Wh)
try:
    pvkwh = response["CounterReadingExport"]
    pvkwh = round(pvkwh * 1000, 3)
except:
    traceback.print_exc()
    exit(1)
# Zur Reduzierung der Datenmenge kann die folgende Zeile eingefügt werden.
# pvkwh=$(echo "$pvkwh / 1" | bc)

# Prüfen ob Werte gültig
regex = '^[-+]?[0-9]+\.?[0-9]*$'
if re.search(regex, wattwr) == None:
    with open("/var/www/html/openWB/ramdisk/pvwatt", "r") as f:
        wattwr = f.read()
if re.search(regex, pvkwh) == None:
    with open("/var/www/html/openWB/ramdisk/pvkwh", "r") as f:
        pvkwh = f.read()


# Ausgabe
if Debug >= 1:
    DebugLog('WR Leistung: ' + str(wattwr))
with open("/var/www/html/openWB/ramdisk/pvwatt", "w") as f:
    f.write(str(wattwr))
if Debug >= 1:
    DebugLog('WR Energie: ' + str(pvkwh))
with open("/var/www/html/openWB/ramdisk/pvkwh", "w") as f:
    f.write(str(pvkwh))
pvkwhk = round(pvkwh / 1000, 3)
with open("/var/www/html/openWB/ramdisk/pvkwhk", "w") as f:
    f.write(str(pvkwhk))

exit(0)