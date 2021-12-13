#!/usr/bin/env python3

from datetime import datetime, timezone
import os
import re
import requests
import sys

Debug = int(os.environ.get('debug'))
myPid = str(os.getpid())

bydhvip = str(sys.argv[1])
bydhvuser = str(sys.argv[2])
bydhvpass = str(sys.argv[3])


def DebugLog(message):
    local_time = datetime.now(timezone.utc).astimezone()
    print(local_time.strftime(format="%Y-%m-%d %H:%M:%S") + ": PID: " + myPid + ": " + message)


if Debug >= 2:
    DebugLog('Speicher IP: ' + bydhvip)
    DebugLog('Speicher User: ' + bydhvuser)
    DebugLog('Speicher Passwort: ' + bydhvpass)

response = requests.get('http://'+bydhvip+'/asp/RunData.asp', auth=(bydhvuser, bydhvpass))
response.encoding = 'utf-8'
response = response.text
response = response.split("\n")
for line in range(len(response)):
    if "SOC:" in response[line]:
        response = response[line:line+2]
        response = ''.join(response)
        response = response.replace("%", "")
        group = re.search("^.*value=$", response).group()
        soc = response.replace(group, "")
        if Debug >= 1:
            DebugLog('Soc: ' + str(soc))
        with open("/var/www/html/openWB/ramdisk/speichersoc", "w") as f:
            f.write(str(soc))
        break

response = requests.get('http://'+bydhvip+'/asp/Home.asp', auth=(bydhvuser, bydhvpass))
response.encoding = 'utf-8'
response = response.text
response = response.split("\n")
for line in range(len(response)):
    if "Power:" in response[line]:
        response = response[line:line+2]
        response = ''.join(response)
        response = response.replace(">", "")
        group = re.search("^.*value=$", response).group()
        speicherleistung = response.replace(group, "")
        speicherleistung = int(speicherleistung*1000)
        if Debug >= 1:
            DebugLog('Speicherleistung: ' + str(speicherleistung))
        with open("/var/www/html/openWB/ramdisk/speicherleistung", "w") as f:
            f.write(str(speicherleistung))
        break
