#!/usr/bin/env python3

from datetime import datetime, timezone
import os
import re
import requests
import sys

Debug = int(os.environ.get('debug'))
myPid = str(os.getpid())

wr_http_w_url = str(sys.argv[1])
wr_http_kwh_url = str(sys.argv[2])

def DebugLog(message):
    local_time = datetime.now(timezone.utc).astimezone()
    print(local_time.strftime(format = "%Y-%m-%d %H:%M:%S") + ": PID: "+ myPid +": " + message)


if Debug >= 2:
    DebugLog('Wechselrichter http URL Leistung: ' + wr_http_w_url)
    DebugLog('Wechselrichter http URL Energie: ' + wr_http_kwh_url)

response = requests.get(wr_http_w_url, timeout=10)
response.encoding = 'utf-8'
wattwr = response.text.replace("\n", "")
regex = '^-?[0-9]+$'
if re.search(regex, wattwr) == None:
    wattwr = 0

if wattwr > 3:
    wattwr = wattwr * -1

if Debug >= 1:
    DebugLog('WR Leistung: ' + str(wattwr))
with open("/var/www/html/openWB/ramdisk/pvwatt", "w") as f:
    f.write(str(wattwr))

if wr_http_kwh_url != "none":
    response = requests.get(wr_http_kwh_url, timeout=5)
    response.encoding = 'utf-8'
    ekwh = response.text.replace("\n", "")
    if Debug >= 1:
        DebugLog('WR Energie: ' + str(ekwh))
    with open("/var/www/html/openWB/ramdisk/pvkwh", "w") as f:
        f.write(str(ekwh))
    pvkwhk = round(ekwh / 1000, 3)
    with open("/var/www/html/openWB/ramdisk/pvkwhk", "w") as f:
        f.write(str(pvkwhk))

exit(0)