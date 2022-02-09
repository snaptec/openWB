#!/usr/bin/env python3
from datetime import datetime, timezone
import os
import requests
import sys
import traceback

wrkostalpikoip = str(sys.argv[1])
speichermodul = str(sys.argv[2])

Debug = int(os.environ.get('debug'))
myPid = str(os.getpid())


def DebugLog(message):
    local_time = datetime.now(timezone.utc).astimezone()
    print(local_time.strftime(format="%Y-%m-%d %H:%M:%S") + ": PID: " + myPid + ": " + message)


if Debug >= 2:
    DebugLog('Kostal Piko IP: ' + wrkostalpikoip)
    DebugLog('Kostal Piko Speicher: ' + speichermodul)

# Auslesen eines Kostal Piko WR über die integrierte API des WR mit angeschlossenem Eigenverbrauchssensor.

params = (
    ('dxsEntries', ['33556736', '251658753', '83887106', '83887362', '83887618']),
)
pvwatttmp = requests.get('http://'+wrkostalpikoip+'/api/dxs.json', params=params, timeout=3).json()
# aktuelle Ausgangsleistung am WR [W]
try:
    pvwatt = int(pvwatttmp["dxsEntries"][0]["value"])
except:
    traceback.print_exc()
    exit(1)
if Debug >= 1:
    DebugLog('Leistung WR: ' + str(pvwatt))

if pvwatt > 5:
    pvwatt = pvwatt*-1

# zur weiteren verwendung im webinterface
with open("/var/www/html/openWB/ramdisk/pvwatt", "w") as f:
    f.write(str(pvwatt))
# Gesamtzählerstand am WR [kWh]
try:
    pvkwh = int(pvwatttmp["dxsEntries"][1]["value"])
except:
    traceback.print_exc()
    exit(1)
if Debug >= 1:
    DebugLog('Zaehlerstand WR: ' + str(pvkwh))

pvkwh = pvkwh*1000
# zur weiteren verwendung im webinterface
with open("/var/www/html/openWB/ramdisk/pvkwh", "w") as f:
    f.write(str(pvkwh))

try:
    bezugw1 = int(pvwatttmp["dxsEntries"][2]["value"])
except:
    traceback.print_exc()
    exit(1)
if Debug >= 1:
    DebugLog('Leistung L1: ' + str(bezugw1))

try:
    bezugw2 = int(pvwatttmp["dxsEntries"][3]["value"])
except:
    traceback.print_exc()
    exit(1)
if Debug >= 1:
    DebugLog('Leistung L2: ' + str(bezugw2))

try:
    bezugw3 = int(pvwatttmp["dxsEntries"][4]["value"])
except:
    traceback.print_exc()
    exit(1)
if Debug >= 1:
    DebugLog('Leistung L3: ' + str(bezugw3))

if speichermodul == "speicher_bydhv":
    with open("/var/www/html/openWB/ramdisk/speicherleistung", "r") as f:
        speicherleistung = f.read()
    wattbezug = bezugw1+bezugw2+bezugw3+pvwatt+int(speicherleistung)
else:
    wattbezug = bezugw1+bezugw2+bezugw3+pvwatt

with open("/var/www/html/openWB/ramdisk/wattbezug", "w") as f:
    f.write(str(wattbezug))
if Debug >= 1:
    DebugLog('Watt: ' + str(wattbezug))
bezuga1 = round((bezugw1 / 225), 2)
bezuga2 = round((bezugw2 / 225), 2)
bezuga3 = round((bezugw3 / 225), 2)
with open("/var/www/html/openWB/ramdisk/bezuga1", "w") as f:
    f.write(str(bezuga1))
with open("/var/www/html/openWB/ramdisk/bezuga2", "w") as f:
    f.write(str(bezuga2))
with open("/var/www/html/openWB/ramdisk/bezuga3", "w") as f:
    f.write(str(bezuga3))
if Debug >= 1:
    DebugLog('Strom L1: ' + str(bezuga1))
    DebugLog('Strom L2: ' + str(bezuga2))
    DebugLog('Strom L3: ' + str(bezuga3))

exit(0)
