#!/usr/bin/env python3

from datetime import datetime, timezone
import os
import re
import requests
import sys
import traceback

Debug = int(os.environ.get('debug'))
myPid = str(os.getpid())

sonnenecoalternativ = str(sys.argv[1])
sonnenecoip = str(sys.argv[2])

def DebugLog(message):
    local_time = datetime.now(timezone.utc).astimezone()
    print(local_time.strftime(format="%Y-%m-%d %H:%M:%S") + ": PID: " + myPid + ": " + message)


if Debug >= 2:
    DebugLog('Speicher Alternativ: ' + sonnenecoalternativ)
    DebugLog('Speicher IP: ' + sonnenecoip)

ra = '^-?[0-9]+$'

def check_write_value(value, file):
    global ra 
    if re.search(ra, value) == None:
        value = "0"
    if Debug >= 1:
        DebugLog(file+': ' + str(value))
    with open("/var/www/html/openWB/ramdisk/"+file, "w") as f:
        f.write(str(value))


# Auslesen einer Sonnbenbatterie Eco 4.5 über die integrierte JSON-API des Batteriesystems
if sonnenecoalternativ == 2:
    response = requests.get('http://'+sonnenecoip+':7979/rest/devices/battery/M05', timeout=5)
    response.encoding = 'utf-8'
    speichersoc = response.text.replace("\n", "")
    speichersoc = int(speichersoc)
    response = requests.get('http://'+sonnenecoip+':7979/rest/devices/battery/M01', timeout=5)
    response.encoding = 'utf-8'
    speicherentladung = response.text.replace("\n", "")
    response = requests.get('http://'+sonnenecoip+':7979/rest/devices/battery/M02', timeout=5)
    response.encoding = 'utf-8'
    speicherladung = response.text.replace("\n", "")
    speicherladung = int(speicherladung)
    speicherentladung = int(speicherentladung)
    speicherwatt = speicherladung - speicherentladung
    # wenn Batterie aus bzw. keine Antwort ersetze leeren Wert durch eine 0
    check_write_value(speicherwatt, "speicherleistung")
    check_write_value(speichersoc, "speichersoc")
    response = requests.get('http://'+sonnenecoip+':7979/rest/devices/battery/M03', timeout=5)
    response.encoding = 'utf-8'
    pvwatt = response.text.replace("\n", "")
    pvwatt = int(pvwatt)
    pvwatt = pvwatt * -1
    if Debug >= 1:
        DebugLog('PV Leistung: ' + str(pvwatt))
    with open("/var/www/html/openWB/ramdisk/pvwatt", "w") as f:
        f.write(str(pvwatt))
else:
    if sonnenecoalternativ == 0:
        speicherantwort = requests.get('http://'+sonnenecoip+':7979/rest/devices/battery', timeout=5).json()
        try:
            speichersoc = int(speicherantwort["M05"])
        except:
            traceback.print_exc()
            exit(1)
        try:
            speicherentladung = int(speicherantwort["M34"])
        except:
            traceback.print_exc()
            exit(1)
        try:
            speicherladung = int(speicherantwort["M35"])
        except:
            traceback.print_exc()
            exit(1)
        speicherwatt = speicherladung - speicherentladung
        # wenn Batterie aus bzw. keine Antwort ersetze leeren Wert durch eine 0
        check_write_value(speicherwatt, "speicherleistung")
        check_write_value(speichersoc, "speichersoc")
    else:
        speicherantwort = requests.get("http://"+sonnenecoip+"/api/v1/status", timeout=5).json()
        try:
            speicherwatt = speicherantwort["Pac_total_W"]
        except:
            traceback.print_exc()
            exit(1)
        try:
            speichersoc = speicherantwort["USOC"]
            if Debug >= 1:
                DebugLog('SpeicherSoC: ' + str(speichersoc))
            if not str(speichersoc).isnumeric():
                DebugLog('SpeicherSoc nicht numerisch. -->0')
                speichersoc = 0
        except:
            traceback.print_exc()
            exit(1)
        try:
            speicherpvwatt = speicherantwort["Production_W"]
        except:
            traceback.print_exc()
            exit(1)
        speicherpvwatt = speicherpvwatt * -1
        if Debug >= 1:
            DebugLog('Speicher PV Watt: ' + str(speicherpvwatt))
        with open("/var/www/html/openWB/ramdisk/pvwatt", "w") as f:
            f.write(str(speicherpvwatt))
        if re.search(ra, speicherwatt) == None:
            speicherwatt = "0"
        else:
            speicherwatt = speicherwatt * -1
        if Debug >= 1:
            DebugLog('Speicherleistung: ' + str(speicherwatt))
        with open("/var/www/html/openWB/ramdisk/speicherleistung", "w") as f:
            f.write(str(speicherwatt))
        check_write_value(speichersoc, "speichersoc")

exit(0)
