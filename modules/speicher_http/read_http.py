#!/usr/bin/env python3

from datetime import datetime, timezone
import os
import requests
import sys
import traceback

Debug = int(os.environ.get('debug'))
myPid = str(os.getpid())

speichersoc_http = str(sys.argv[1])
speicherleistung_http = str(sys.argv[2])
speicherikwh_http = str(sys.argv[3])
speicherekwh_http = str(sys.argv[4])


def DebugLog(message):
    local_time = datetime.now(timezone.utc).astimezone()
    print(local_time.strftime(format="%Y-%m-%d %H:%M:%S") + ": PID: " + myPid + ": " + message)


if Debug >= 2:
    DebugLog('Speicher URL Soc: ' + speichersoc_http)
    DebugLog('Speicher URL Leistung: ' + speicherleistung_http)
    DebugLog('Speicher URL Import: ' + speicherikwh_http)
    DebugLog('Speicher URL Export: ' + speicherikwh_http)

try:
    response = requests.get(speichersoc_http, timeout=10)
    response.encoding = 'utf-8'
    soc = int(response.text.replace("\n", ""))
    if Debug >= 1:
        DebugLog('SpeicherSoC: ' + str(soc))
    if not str(soc).isnumeric():
        DebugLog('SpeicherSoc nicht numerisch. -->0')
        soc = 0
    with open("/var/www/html/openWB/ramdisk/speichersoc", "w") as f:
        f.write(str(soc))
except:
    traceback.print_exc()
    exit(1)

try:
    response = requests.get(speicherleistung_http, timeout=10)
    response.encoding = 'utf-8'
    leistung = response.text.replace("\n", "")
    if Debug >= 1:
        DebugLog('Speicherleistung: ' + str(leistung))
    with open("/var/www/html/openWB/ramdisk/speicherleistung", "w") as f:
        f.write(str(leistung))
except:
    traceback.print_exc()
    exit(1)

if speicherikwh_http != "none":
    try:
        response = requests.get(speicherikwh_http, timeout=10)
        response.encoding = 'utf-8'
        ikwh = response.text.replace("\n", "")
        if Debug >= 1:
            DebugLog('Speicher Import: ' + str(ikwh))
        with open("/var/www/html/openWB/ramdisk/speicherikwh", "w") as f:
            f.write(str(ikwh))
    except:
        traceback.print_exc()
        exit(1)

if speicherekwh_http != "none":
    try:
        response = requests.get(speicherekwh_http, timeout=10)
        response.encoding = 'utf-8'
        ekwh = response.text.replace("\n", "")
        if Debug >= 1:
            DebugLog('Speicher Export: ' + str(ekwh))
        with open("/var/www/html/openWB/ramdisk/speicherekwh", "w") as f:
            f.write(str(ekwh))
    except:
        traceback.print_exc()
        exit(1)

exit(0)
