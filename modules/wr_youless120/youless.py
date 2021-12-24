#!/usr/bin/env python3
from datetime import datetime, timezone
import os
import requests
import sys
import traceback

Debug = int(os.environ.get('debug'))
myPid = str(os.getpid())

wryoulessip = str(sys.argv[1])
wryoulessalt = str(sys.argv[2])


def DebugLog(message):
    local_time = datetime.now(timezone.utc).astimezone()
    print(local_time.strftime(format="%Y-%m-%d %H:%M:%S") + ": PID: " + myPid + ": " + message)


if Debug >= 2:
    DebugLog('PV Youless IP:' + wryoulessip)
    DebugLog('PV Youless Alternative:' + wryoulessalt)

# Auslesen vom S0-Eingang eines Youless LS120 Energy Monitor.
params = (('f', 'j'),)
answer = requests.get("http://"+wryoulessip+'/a', params=params, timeout=5).json()
if wryoulessalt == 0:
    try:
        # aktuelle Ausgangsleistung am WR [W]
        pvwatt = int(answer["ps0"])
        # Gesamtz‰hlerstand am WR [Wh]
        pvkwh = answer["cs0"]
        pvkwh = pvkwh.replace(",", "")
    except:
        traceback.print_exc()
        exit(1)
else:
    try:
        # aktuelle Ausgangsleistung am WR [W]
        pvwatt = int(answer["pwr"])
        # Gesamtz‰hlerstand am WR [Wh]
        pvkwh = answer["cnt"]
        pvkwh = pvkwh.replace(",", "")
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
# Gesamtzählerstand am WR [kWh]
pvkwh = pvkwh/1000
with open("/var/www/html/openWB/ramdisk/pvkwhk", "w") as f:
    f.write(str(pvkwh))

exit(0)
