#!/usr/bin/env python3

from datetime import datetime, timezone
import os
import requests
import sys

from modules.common.component_state import InverterState
from modules.common.store import get_inverter_value_store

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

# Auslesen eines Kostal Piko WR über die integrierte API des WR. Rückgabewert ist die aktuelle Wattleistung.
if speichermodul != "none":
    params = (('dxsEntries', ['33556736', '251658753)']),)
    pvwatttmp = requests.get('http://'+wrkostalpikoip+'/api/dxs.json', params=params, timeout=5).json()
else:
    params = (('dxsEntries', ['67109120', '251658753)']),)
    pvwatttmp = requests.get('http://'+wrkostalpikoip+'/api/dxs.json', params=params, timeout=5).json()

# aktuelle Ausgangsleistung am WR [W]
pvwatt = int(pvwatttmp["dxsEntries"][0]["value"])

if pvwatt > 5:
    pvwatt = pvwatt*-1

if Debug >= 1:
    DebugLog('WR Leistung: ' + str(pvwatt))
# Gesamtzählerstand am WR [kWh]
pvkwh = int(pvwatttmp['dxsEntries'][1]['value'])

get_inverter_value_store(num).set(InverterState(counter=pvkwh*1000, power=pvwatt))
