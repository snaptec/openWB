#!/usr/bin/env python3
from datetime import datetime, timezone
import os
import re
import requests
import sys
import traceback

bezug_smartme_url = str(sys.argv[1])
bezug_smartme_user = str(sys.argv[2])
bezug_smartme_pass = str(sys.argv[3])

Debug = int(os.environ.get('debug'))
myPid = str(os.getpid())


def DebugLog(message):
    local_time = datetime.now(timezone.utc).astimezone()
    print(local_time.strftime(format="%Y-%m-%d %H:%M:%S") + ": PID: " + myPid + ": " + message)


if Debug >= 2:
    DebugLog('Smartme URL: ' + bezug_smartme_url)
    DebugLog('Smartme User: ' + bezug_smartme_user)
    DebugLog('Smartme Passwort: ' + bezug_smartme_pass)


def get_power_value(key, file=None):
    try:
        value = int(response[key] * 1000)
        if file == None:
            return value
        else:
            if Debug >= 1:
                DebugLog(file+': ' + str(value))
            f = open('/var/www/html/openWB/ramdisk/'+file, 'w')
            f.write(str(value))
            f.close()
    except:
        traceback.print_exc()
        exit(1)


def get_im_ex_value(key, file=None):
    try:
        value = round(response[key] * 1000, 3)
        if Debug >= 1:
            DebugLog(file+': ' + str(value))
        f = open('/var/www/html/openWB/ramdisk/'+file, 'w')
        f.write(str(value))
        f.close()
    except:
        traceback.print_exc()
        exit(1)


def get_value(key, file=None):
    try:
        value = response[key]
        if file == None:
            return value
        else:
            if Debug >= 1:
                DebugLog(file+': ' + str(value))
            f = open('/var/www/html/openWB/ramdisk/'+file, 'w')
            f.write(str(value))
            f.close()
    except:
        traceback.print_exc()
        exit(1)


# Daten einlesen
response = requests.get(bezug_smartme_url, auth=(bezug_smartme_user, bezug_smartme_pass), timeout=10).json()

# Aktuelle Leistung (kW --> W)
wattbezug = get_power_value("ActivePower")
wattbezug1 = get_power_value("ActivePowerL1")
if wattbezug1 == 0:
    wattbezug1 = wattbezug
get_power_value("ActivePowerL2", "bezugw2")
get_power_value("ActivePowerL3", "bezugw3")
# Zählerstand Import(kWh)
get_im_ex_value("CounterReadingImport", "bezugkwh")
# Zählerstand Export(kWh)
get_im_ex_value("CounterReadingExport", "einspeisungkwh")

# Weitere Zählerdaten für die Statusseite (PowerFaktor, Spannung und Strom)
get_value("PowerFactorL1", "evupf1")
get_value("PowerFactorL2", "evupf2")
get_value("PowerFactorL3", "evupf3")
get_value("VoltageL1", "evuv1")
get_value("VoltageL2", "evuv2")
get_value("VoltageL3", "evuv3")
bezuga1 = get_value("CurrentL1")
if bezuga1 is None:
    try:
        bezuga1 = response["Current"]
    except:
        traceback.print_exc()
        exit(1)
if Debug >= 1:
    DebugLog('Strom L1: ' + str(bezuga1))
with open("/var/www/html/openWB/ramdisk/bezuga1", "w") as f:
    f.write(str(bezuga1))
get_value("CurrentL2", "bezuga2")
get_value("CurrentL3", "bezuga3")


# Prüfen ob Werte gültig
regex = '^[-+]?[0-9]+\.?[0-9]*$'
if re.search(regex, str(wattbezug)) == None:
    with open("/var/www/html/openWB/ramdisk/wattbezug", "r") as f:
        wattbezug = f.read()
# Ausgabe
if Debug >= 1:
    DebugLog('Leistung: ' + str(wattbezug))
with open("/var/www/html/openWB/ramdisk/wattbezug", "w") as f:
    f.write(str(wattbezug))
if Debug >= 1:
    DebugLog('Leistung L1: ' + str(wattbezug1))
with open("/var/www/html/openWB/ramdisk/wattbezugw1", "w") as f:
    f.write(str(wattbezug1))

exit(0)
