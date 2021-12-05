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

# Auslesen eines Fronius Symo WR über die integrierte API des WR.
# Rückgabewert ist die aktuelle Wirkleistung in [W].
response = requests.get('http://'+wrfroniusip+'/solar_api/v1/GetPowerFlowRealtimeData.fcgi', params=params, timeout=3)
pvwatttmp = response.json()
DebugLog(1, 'response: ' + str(response))
DebugLog(2, 'response_pvwatt: ' + str(pvwatttmp))
# Ohne PV Produktion liefert der WR 'null', ersetze durch Zahl 0
pvwatt = pvwatttmp["Body"]["Data"]["Site"]["P_PV"] or 0

if wrfroniusisgen24 == "0":
    pvkwh_start = 0
    pvkwh_offset = 0
    pvkwh = pvwatttmp["Body"]["Data"]["Site"]["E_Total"]
    pvday = pvwatttmp["Body"]["Data"]["Site"]["E_Day"]
    try:
        with open("/var/www/html/openWB/ramdisk/pvkwh_offset", "r") as f:
            pvkwh_offset = int(f.read())
    except FileNotFoundError as e:
        DebugLog(1, str(e))
    try:
        with open("/var/www/html/openWB/ramdisk/pvkwh_start", "r") as f:
            pvkwh_start = int(f.read())
        pvkwh_new = pvkwh_start + pvday + pvkwh_offset
        if pvkwh_new > pvkwh:
            if pvkwh_new - pvkwh >= 100:
                # Korregiere Abweichung
                pvkwh_diff = pvkwh_new - pvkwh - 99
                pvkwh_offset -= pvkwh_diff
                pvkwh_new -= pvkwh_diff
            pvkwh = pvkwh_new
        else:
            # Berechne Abweichung als Mittelwert von aktueller und bisheriger Abweichung
            pvkwh_offset = round((pvkwh_offset + pvkwh - pvkwh_start - pvday) / 2)
    except FileNotFoundError as e:
        DebugLog(1, str(e))

if wrfronius2ip != "none":
    response = requests.get('http://'+wrfronius2ip+'/solar_api/v1/GetPowerFlowRealtimeData.fcgi', params=params, timeout=3)
    pv2watttmp = response.json()
    DebugLog(1, 'response: ' + str(response))
    DebugLog(2, 'response_pv2watt: ' + str(pv2watttmp))
    # Ohne PV Produktion liefert der WR 'null', ersetze durch Zahl 0
    pv2watt = pv2watttmp["Body"]["Data"]["Site"]["P_PV"] or 0
    pvwatt = (pvwatt + pv2watt) * -1
    DebugLog(2, 'pvwatt: ' + str(pvwatt))
    # Zur weiteren Verwendung im Webinterface
    with open("/var/www/html/openWB/ramdisk/pvwatt", "w") as f:
        f.write(str(pvwatt))
    if wrfroniusisgen24 == "0":
        pv2kwh = pv2watttmp["Body"]["Data"]["Site"]["E_Total"]
        pvgkwh = pvkwh + pv2kwh
        if pvgkwh > 0:
            with open("/var/www/html/openWB/ramdisk/pvkwh", "w") as f:
                f.write(str(pvgkwh))
            with open("/var/www/html/openWB/ramdisk/pvkwhk", "w") as f:
                f.write('{:.3f}'.format(pvgkwh / 1000))
else:
    pvwatt *= -1
    DebugLog(2, 'pvwatt: ' + str(pvwatt))
    # Zur weiteren Verwendung im Webinterface
    with open("/var/www/html/openWB/ramdisk/pvwatt", "w") as f:
        f.write(str(pvwatt))
    if wrfroniusisgen24 == "0" and pvkwh > 0:
        if pvday == 0 and pvkwh > pvkwh_start + pvkwh_offset:
            with open("/var/www/html/openWB/ramdisk/pvkwh_start", "w") as f:
                f.write(str(pvkwh))
            with open("/var/www/html/openWB/ramdisk/pvkwh_offset", "w") as f:
                with open("/var/www/html/openWB/ramdisk/pvkwh", "r") as ff:
                    pvkwh_offset = int(ff.read()) - pvkwh
                    pvkwh += pvkwh_offset
                    f.write(str(pvkwh_offset))
        else:
            with open("/var/www/html/openWB/ramdisk/pvkwh_offset", "w") as f:
                f.write(str(pvkwh_offset))
        with open("/var/www/html/openWB/ramdisk/pvkwh", "w") as f:
            f.write(str(pvkwh))
        with open("/var/www/html/openWB/ramdisk/pvkwhk", "w") as f:
            f.write('{:.3f}'.format(pvkwh / 1000))

exit(0)