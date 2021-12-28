#!/usr/bin/env python3
import os
import sys
from datetime import datetime, timezone

import requests

from modules.common.component_state import InverterState
from modules.common.store import get_inverter_value_store

Debug = int(os.environ.get('debug'))
myPid = str(os.getpid())

wr_smartme_url = str(sys.argv[1])
wr_smartme_user = str(sys.argv[2])
wr_smartme_pass = str(sys.argv[3])


def DebugLog(message):
    local_time = datetime.now(timezone.utc).astimezone()
    print(local_time.strftime(format="%Y-%m-%d %H:%M:%S") + ": PID: " + myPid + ": " + message)


if Debug >= 2:
    DebugLog('Wechselrichter smartme URL: ' + wr_smartme_url)
    DebugLog('Wechselrichter smartme User: ' + wr_smartme_user)
    DebugLog('Wechselrichter smartme Passwort: ' + wr_smartme_pass)

# Daten einlesen
response = requests.get(wr_smartme_url, auth=(wr_smartme_user, wr_smartme_pass), timeout=10).json()
# Aktuelle Leistung (kW --> W)
wattwr = response["ActivePower"]
wattwr = round(wattwr * 1000)

# Zählerstand Export (kWh --> Wh)
pvkwh = response["CounterReadingExport"]
pvkwh = round(pvkwh * 1000, 3)


if Debug >= 1:
    DebugLog('WR Leistung: ' + str(wattwr))
    DebugLog('WR Energie: ' + str(pvkwh))

get_inverter_value_store(1).set(InverterState(counter=pvkwh, power=wattwr))
