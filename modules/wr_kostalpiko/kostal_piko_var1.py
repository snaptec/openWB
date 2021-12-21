#!/usr/bin/env python3

from datetime import datetime, timezone
import os
import requests
import sys
import traceback

Debug = int(os.environ.get('debug'))
myPid = str(os.getpid())

num = int(sys.argv[1])
speichermodul = str(sys.argv[2])
wrkostalpikoip = str(sys.argv[3])


def DebugLog(message):
    local_time = datetime.now(timezone.utc).astimezone()
    print(local_time.strftime(format="%Y-%m-%d %H:%M:%S") + ": PID: " + myPid + ": " + message)


if Debug >= 2:
    DebugLog('Wechselrichter Kostal Piko Var 1 Speicher: ' + speichermodul)
    DebugLog('Wechselrichter Kostal Piko Var 1 IP: ' + wrkostalpikoip)

if num == 1:
    file_ext = ""
elif num == 2:
    file_ext = "2"

# Auslesen eines Kostal Piko WR über die integrierte API des WR. Rückgabewert ist die aktuelle Wattleistung.
if speichermodul != "none":
    params = (('dxsEntries', ['33556736', '251658753)']),)
    pvwatttmp = requests.get('http://'+wrkostalpikoip+'/api/dxs.json', params=params, timeout=5).json()
else:
    params = (('dxsEntries', ['67109120', '251658753)']),)
    pvwatttmp = requests.get('http://'+wrkostalpikoip+'/api/dxs.json', params=params, timeout=5).json()

# aktuelle Ausgangsleistung am WR [W]
try:
    pvwatt = int(pvwatttmp["dxsEntries"][0]["value"])
except:
    traceback.print_exc()
    exit(1)
if pvwatt > 5:
    pvwatt = pvwatt*-1

# zur weiteren verwendung im webinterface
if Debug >= 1:
    DebugLog('WR Leistung: ' + str(pvwatt))
with open("/var/www/html/openWB/ramdisk/pv"+file_ext+"watt", "w") as f:
    f.write(str(pvwatt))
# Gesamtzählerstand am WR [kWh]
pvkwh = int(pvwatttmp['dxsEntries'][1]['value'])
with open("/var/www/html/openWB/ramdisk/pv"+file_ext+"kwhk", "w") as f:
    f.write(str(pvkwh))

pvkwh = pvkwh*1000
# zur weiteren verwendung im webinterface
with open("/var/www/html/openWB/ramdisk/pv"+file_ext+"kwh", "w") as f:
    f.write(str(pvkwh))


exit(0)
