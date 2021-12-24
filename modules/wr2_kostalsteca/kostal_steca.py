#!/usr/bin/env python3
from datetime import datetime, timezone
import os
import xml.etree.ElementTree as ET
import re
import requests
import subprocess
import sys

Debug = int(os.environ.get('debug'))
myPid = str(os.getpid())

pv2ip = str(sys.argv[1])
#
# RainerW 8th of April 2020
# Unfortunately Kostal has introduced the third version of interface: XML
# This script is for Kostal_Piko_MP_plus and StecaGrid coolcept (single phase inverter)
# In fact Kostal is not developing own single phase inverter anymore but is sourcing them from Steca
# If you have the chance to test this module for the latest three phase inverter from Kostal (Plenticore) or Steca (coolcept3 or coolcept XL) let us know if it works
# DetMoerk 20210323: Anpassung fuer ein- und dreiphasige WR der Serie. Anstatt eine feste Zeile aus dem Ergebnis zu schneiden wird nach der Zeile mit AC_Power gesucht.


def DebugLog(message):
    local_time = datetime.now(timezone.utc).astimezone()
    print(local_time.strftime(format="%Y-%m-%d %H:%M:%S") + ": PID: " + myPid + ": " + message)


if Debug >= 2:
    DebugLog('PV Kostal Steca IP:' + pv2ip)


# call for XML file and parse it for current PV power
response = requests.get("http://"+pv2ip+"/measurements.xml", timeout=5).text
if Debug >= 1:
    DebugLog("MEASURE: "+str(response))
power_kostal_piko_MP = ET.fromstring(response).find("Measurement[@Type='AC_Power']").get("Value")

# cut the comma and the digit behind the comma
power_kostal_piko_MP = int(float(power_kostal_piko_MP))

# allow only numbers
regex = '^-?[0-9]+$'
if re.search(regex, str(power_kostal_piko_MP)) == None:
    power_kostal_piko_MP = "0"

DebugLog("'PVWatt: "+str(power_kostal_piko_MP)+"'")

# call for XML file and parse it for total produced kwh
if Debug > 1:
    yields = requests.get("http://"+pv2ip+"/yields.xml", timeout=5).text
    DebugLog("YIELD: "+yields)

response = requests.get("http://"+pv2ip+"/yields.xml", timeout=5).text
pvkwh_kostal_piko_MP = ET.fromstring(response).find("YieldValue").get("Value")

if re.search(regex, str(pvkwh_kostal_piko_MP)) == None:
    DebugLog("PVkWh: NaN get prev. Value")
    with open("/var/www/html/openWB/ramdisk/pv2kwh", "r") as f:
        pvkwh_kostal_piko_MP = f.read()

DebugLog('PVkWh: '+str(pvkwh_kostal_piko_MP))

# Daten in Ramdisk schreiben
if Debug >= 1:
    DebugLog('WR Energie: ' + str(pvkwh_kostal_piko_MP))
with open("/var/www/html/openWB/ramdisk/pv2kwh", "w") as f:
    f.write(str(pvkwh_kostal_piko_MP))
if Debug >= 1:
    DebugLog('WR Leistung: ' + "-"+str(power_kostal_piko_MP))
with open("/var/www/html/openWB/ramdisk/pv2watt", "w") as f:
    f.write("-"+str(power_kostal_piko_MP))

exit(0)
