#!/usr/bin/env python3

from datetime import datetime, timezone
import os
import re
import requests
import sys
import traceback

Debug = int(os.environ.get('debug'))
myPid = str(os.getpid())

wrfroniusip = str(sys.argv[1])
wrfroniusisgen24 = int(sys.argv[2])
wrfronius2ip = str(sys.argv[3])

def DebugLog(message):
    local_time = datetime.now(timezone.utc).astimezone()
    print(local_time.strftime(format = "%Y-%m-%d %H:%M:%S") + ": PID: "+ myPid +": " + message)


if Debug >= 2:
    DebugLog('Wechselrichter Fronius IP: ' + wrfroniusip)
    DebugLog('Wechselrichter Fronius Gen 24: ' + wrfroniusisgen24)
    DebugLog('Wechselrichter Fronius IP2: ' + wrfronius2ip)

# Auslesen eine Fronius Symo WR über die integrierte API des WR. Rückgabewert ist die aktuelle Wirkleistung in [W].
params = (
    ('Scope', 'System'),
)
pvwatttmp = requests.get('http://'+wrfroniusip+'/solar_api/v1/GetPowerFlowRealtimeData.fcgi', params=params, timeout=3).json()
try:
    pvwatt = int(pvwatttmp["Body"]["Data"]["Site"]["P_PV"])
except:
    traceback.print_exc()
    exit(1)

# Wenn WR aus bzw. im Standby (keine Antwort), ersetze leeren Wert durch eine 0
regex = '^-?[0-9]+$'
if re.search(regex, pvwatt) == None:
    pvwatt = "0"

if wrfroniusisgen24 == 0:
    try:
        pvkwh = int(pvwatttmp["Body"]["Data"]["Site"]["E_Total"])
    except:
        traceback.print_exc()
        exit(1)

if wrfronius2ip != "none":
    params = (('Scope', 'System'),)
    pv2watttmp = requests.get('http://'+wrfronius2ip+'/solar_api/v1/GetPowerFlowRealtimeData.fcgi', params=params, timeout=3).json()
    try:
        pv2watt = int(pv2watttmp["Body"]["Data"]["Site"]["P_PV"])
    except:
        traceback.print_exc()
        exit(1)
    # Wenn WR aus bzw. im Standby (keine Antwort), ersetze leeren Wert durch eine 0
    regex = '^-?[0-9]+$'
    if re.search(regex, pv2watt) == None:
        pv2watt = "0"
    pvwatt = (pvwatt + pv2watt) * -1
    # Zur weiteren Verwendung im Webinterface
    if Debug >= 1:
        DebugLog('WR Leistung: ' + str(pvwatt))
    with open("/var/www/html/openWB/ramdisk/pvwatt", "w") as f:
        f.write(str(pvwatt))
    if wrfroniusisgen24 == 0:
        try:
            pv2kwh = int(pv2watttmp["Body"]["Data"]["Site"]["E_Total"])
        except:
            traceback.print_exc()
            exit(1)
        pvgkwh = pvkwh + pv2kwh
        if re.search(regex, pvgkwh) != None:
            if pvgkwh > 0:
                if Debug >= 1:
                    DebugLog('WR Energie: ' + str(pvgkwh))
                with open("/var/www/html/openWB/ramdisk/pvkwh", "w") as f:
                    f.write(str(pvgkwh))
                pvkwhk = round(pvgkwh / 1000, 3)
                with open("/var/www/html/openWB/ramdisk/pvkwhk", "w") as f:
                    f.write(str(pvkwhk))
else:
    pvwatt = pvwatt * -1
    # Zur weiteren Verwendung im Webinterface
    if Debug >= 1:
        DebugLog('WR Leistung: ' + str(pvwatt))
    with open("/var/www/html/openWB/ramdisk/pvwatt", "w") as f:
        f.write(str(pvwatt))
    if wrfroniusisgen24 == 0:
        if re.search(regex, pvkwh) != None:
            if pvkwh > 0:
                if Debug >= 1:
                    DebugLog('WR Energie: ' + str(pvkwh))
                with open("/var/www/html/openWB/ramdisk/pvkwh", "w") as f:
                    f.write(str(pvkwh))
                pvkwhk = round(pvkwh / 1000, 3)
                with open("/var/www/html/openWB/ramdisk/pvkwhk", "w") as f:
                    f.write(str(pvkwhk))

exit(0)