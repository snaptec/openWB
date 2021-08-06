#!/usr/bin/env python3

import requests
import sys
import traceback

battjsonurl = str(sys.argv[1])
battjsonwatt = str(sys.argv[2]).replace(".", "")
battjsonsoc = str(sys.argv[3]).replace(".", "")

response = requests.get(battjsonurl, timeout=5).json()
try:
    speicherleistung = int(response[battjsonwatt])
    with open("/var/www/html/openWB/ramdisk/speicherleistung", "w") as f:
        f.write(str(speicherleistung))
except:
    traceback.print_exc()

try:
    if battjsonsoc != "":
        battsoc = response[battjsonsoc]
    else:
        battsoc = 0
    with open("/var/www/html/openWB/ramdisk/speichersoc", "w") as f:
        f.write(str(battsoc))
except:
    traceback.print_exc()
