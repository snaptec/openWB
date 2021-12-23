#!/usr/bin/env python3

from datetime import datetime, timezone
import os
import requests
import sys

Debug = int(os.environ.get('debug'))
myPid = str(os.getpid())

wrfroniusip = str(sys.argv[1])
wrfroniusisgen24 = int(sys.argv[2])
wrfronius2ip = str(sys.argv[3])

def DebugLog(level, message):
    if Debug >= level:
        local_time = datetime.now(timezone.utc).astimezone()
        print(local_time.strftime(format = "%Y-%m-%d %H:%M:%S") + ": PID: " + myPid + ": " + message)

DebugLog(2, 'WechselrichterFronius IP: ' + wrfroniusip)
DebugLog(2, 'WechselrichterFronius Gen24: ' + str(wrfroniusisgen24))
DebugLog(2, 'WechselrichterFronius 2 IP: ' + wrfronius2ip)

# Auslesen eines Fronius Symo WR über die integrierte API des WR.
# Rückgabewert ist die aktuelle Wirkleistung in [W].
params = (
    ('Scope', 'System'),
)
response = requests.get('http://'+wrfroniusip+'/solar_api/v1/GetPowerFlowRealtimeData.fcgi', params=params, timeout=3)
pvwatttmp = response.json()
DebugLog(1, 'response: ' + str(response))
DebugLog(2, 'response_pvwatt: ' + str(pvwatttmp))
# Ohne PV Produktion liefert der WR 'null', ersetze durch Zahl 0
pvwatt = int(pvwatttmp["Body"]["Data"]["Site"]["P_PV"] or 0)

if wrfroniusisgen24 == 0:
    pvkwh_start = 0
    pvkwh_offset = 0
    pvkwh = int(pvwatttmp["Body"]["Data"]["Site"]["E_Total"])
    pvday = int(pvwatttmp["Body"]["Data"]["Site"]["E_Day"])
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
                # Korrigiere Abweichung
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
    params = (('Scope', 'System'),)
    response = requests.get('http://'+wrfronius2ip+'/solar_api/v1/GetPowerFlowRealtimeData.fcgi', params=params, timeout=3)
    pv2watttmp = response.json()
    DebugLog(1, 'response: ' + str(response))
    DebugLog(2, 'response_pv2watt: ' + str(pv2watttmp))
    # Ohne PV Produktion liefert der WR 'null', ersetze durch Zahl 0
    pv2watt = int(pv2watttmp["Body"]["Data"]["Site"]["P_PV"] or 0)
    pvwatt = (pvwatt + pv2watt) * -1
    # Zur weiteren Verwendung im Webinterface
    DebugLog(1, 'WR Leistung: ' + str(pvwatt))
    with open("/var/www/html/openWB/ramdisk/pvwatt", "w") as f:
        f.write(str(pvwatt))
    if wrfroniusisgen24 == 0:
        pv2kwh = int(pv2watttmp["Body"]["Data"]["Site"]["E_Total"])
        pvgkwh = pvkwh + pv2kwh
        if pvgkwh > 0:
            DebugLog(1, 'WR Energie: ' + str(pvgkwh))
            with open("/var/www/html/openWB/ramdisk/pvkwh", "w") as f:
                f.write(str(pvgkwh))
            with open("/var/www/html/openWB/ramdisk/pvkwhk", "w") as f:
                f.write('{:.3f}'.format(pvgkwh / 1000))
else:
    pvwatt *= -1
    # Zur weiteren Verwendung im Webinterface
    DebugLog(1, 'WR Leistung: ' + str(pvwatt))
    with open("/var/www/html/openWB/ramdisk/pvwatt", "w") as f:
        f.write(str(pvwatt))
    if wrfroniusisgen24 == 0 and pvkwh > 0:
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
        DebugLog(1, 'WR Energie: ' + str(pvkwh))
        with open("/var/www/html/openWB/ramdisk/pvkwh", "w") as f:
            f.write(str(pvkwh))
        pvkwhk = round(pvkwh / 1000, 3)
        with open("/var/www/html/openWB/ramdisk/pvkwhk", "w") as f:
            f.write(str(pvkwhk))

exit(0)