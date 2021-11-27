#!/usr/bin/env python3
from datetime import datetime, timezone
import os
import requests
import sys
import traceback

wrfroniusip = str(sys.argv[1])
wrfronius2ip = str(sys.argv[2])
wrfroniusisgen24 = str(sys.argv[3])

Debug = int(os.environ.get('debug'))
# Debug = 2
myPid = str(os.getpid())


def DebugLog(level, message):
    if Debug >= level:
        local_time = datetime.now(timezone.utc).astimezone()
        print(local_time.strftime(format="%Y-%m-%d %H:%M:%S") + ": PID: " + myPid + ": " + message)


DebugLog(2, 'Fronius IP: ' + wrfroniusip)
DebugLog(2, 'Fronius 2 IP: ' + wrfronius2ip)
DebugLog(2, 'Fronius Gen24: ' + wrfroniusisgen24)

params = (
    ('Scope', 'System'),
)
regex='^-?[0-9]+$'

# Auslesen eines Fronius Symo WR über die integrierte API des WR.
# Rückgabewert ist die aktuelle Wirkleistung in [W].
response = requests.get('http://'+wrfroniusip+'/solar_api/v1/GetPowerFlowRealtimeData.fcgi', params=params, timeout=3)
pvwatttmp = response.json()
DebugLog(1, 'response: ' + str(response))
DebugLog(2, 'response_pvwatt: ' + str(pvwatttmp))
try:
    pvwatt = int(pvwatttmp["Body"]["Data"]["Site"]["P_PV"])
except:
    # Wenn WR aus bzw. im Standby (keine Antwort), ersetze leeren Wert durch eine 0
    pvwatt = 0

if wrfroniusisgen24 == "0":
    try:
	    pvkwh = int(pvwatttmp["Body"]["Data"]["Site"]["E_Total"])
    except:
        traceback.print_exc()
        exit(1)

if wrfronius2ip != "none":
    try:
        response = requests.get('http://'+wrfronius2ip+'/solar_api/v1/GetPowerFlowRealtimeData.fcgi', params=params, timeout=3)
        pv2watttmp = response.json()
        DebugLog(1, 'response: ' + str(response))
        DebugLog(2, 'response_pv2watt: ' + str(pv2watttmp))
        pv2watt = int(pv2watttmp["Body"]["Data"]["Site"]["P_PV"])
    except:
        # Wenn WR aus bzw. im Standby (keine Antwort), ersetze leeren Wert durch eine 0
        pv2watt = 0
    pvwatt = (pvwatt + pv2watt) * -1
    DebugLog(2, 'pvwatt: ' + str(pvwatt))
    # Zur weiteren Verwendung im Webinterface
    with open("/var/www/html/openWB/ramdisk/pvwatt", "w") as f:
        f.write(str(pvwatt))
    if wrfroniusisgen24 == "0":
        try:
            pv2kwh = int(pv2watttmp["Body"]["Data"]["Site"]["E_Total"])
        except:
            pv2kwh = 0
        pvgkwh = pvkwh + pv2kwh
        if pvgkwh > 0:
            with open("/var/www/html/openWB/ramdisk/pvkwh", "w") as f:
                f.write(str(pvgkwh))
            with open("/var/www/html/openWB/ramdisk/pvkwhk", "w") as f:
                f.write('{:.3f}'.format(round(pvgkwh / 1000, 3)))
else:
    pvwatt *= -1
    DebugLog(2, 'pvwatt: ' + str(pvwatt))
    # Zur weiteren Verwendung im Webinterface
    with open("/var/www/html/openWB/ramdisk/pvwatt", "w") as f:
        f.write(str(pvwatt))
    if wrfroniusisgen24 == "0":
        if pvkwh > 0:
            with open("/var/www/html/openWB/ramdisk/pvkwh", "w") as f:
                f.write(str(pvkwh))
            with open("/var/www/html/openWB/ramdisk/pvkwhk", "w") as f:
                f.write('{:.3f}'.format(round(pvkwh / 1000, 3)))

exit(0)