#!/usr/bin/env python3
from datetime import datetime, timezone
import os
import re
import requests
import sys
import traceback

Debug         = int(os.environ.get('debug'))
myPid         = str(os.getpid())

def DebugLog(message):
    local_time = datetime.now(timezone.utc).astimezone()
    print(local_time.strftime(format = "%Y-%m-%d %H:%M:%S") + ": PID: "+ myPid +": " + message)

def get_value(url, file):
    try:
        if url != "none":
            response = requests.get(url, timeout=5)
            response.encoding = 'utf-8'
            value = response.text.replace("\n", "")
            with open("/var/www/html/openWB/ramdisk/"+file, "w") as f:
                f.write(str(value))
    except:
        traceback.print_exc()
        exit(1)
    if Debug >= 1:
        DebugLog(file+': ' + str(wattbezug))


bezug_http_w_url = str(sys.argv[1])
bezug_http_ikwh_url = str(sys.argv[2])
bezug_http_ekwh_url = str(sys.argv[3])
bezug_http_l1_url = str(sys.argv[4])
bezug_http_l2_url = str(sys.argv[5])
bezug_http_l3_url = str(sys.argv[6])

if Debug >= 2:
    DebugLog('http Watt: ' + bezug_http_w_url)
    DebugLog('http Bezug: ' + bezug_http_ikwh_url)
    DebugLog('http Einsp: ' + bezug_http_ekwh_url)
    DebugLog('http Strom L1: ' + bezug_http_l1_url)
    DebugLog('http Strom L2: ' + bezug_http_l2_url)
    DebugLog('http Strom L3: ' + bezug_http_l3_url)

try:
    response = requests.get(bezug_http_w_url, timeout=10)
    response.encoding = 'utf-8'
    wattbezug = response.text.replace("\n", "")
    regex = '^-?[0-9]+$'
    if re.search(regex, wattbezug) == None:
        wattbezug = "0"
    with open("/var/www/html/openWB/ramdisk/wattbezug", "w") as f:
        f.write(str(wattbezug))
except:
    traceback.print_exc()
    exit(1)
if Debug >= 1:
    DebugLog('Watt: ' + str(wattbezug))

get_value(bezug_http_ikwh_url, "bezugkwh")
get_value(bezug_http_ekwh_url, "einspeisungkwh")
get_value(bezug_http_l1_url, "bezuga1")
get_value(bezug_http_l2_url, "bezuga2")
get_value(bezug_http_l3_url, "bezuga3")

exit(0)