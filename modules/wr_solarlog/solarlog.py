#!/usr/bin/env python3

from datetime import datetime, timezone
import os
import json
import requests
import sys

from modules.common.component_state import InverterState
from modules.common.store import get_inverter_value_store

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
pvwatt = response["801"]["170"]["101"]
pvkwh = response["801"]["170"]["109"]

if pvwatt > 5:
    pvwatt = pvwatt*-1

if Debug >= 1:
    DebugLog('WR Leistung: ' + str(pvwatt))
    DebugLog('WR Energie: ' + str(pvkwh))

get_inverter_value_store(1).set(InverterState(counter=pvkwh, power=pvwatt))
