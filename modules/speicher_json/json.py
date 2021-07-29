#!/usr/bin/env python3

import json
import requests
import sys

battjsonurl = str(sys.argv[1])
battjsonwatt = str(sys.argv[2]).replace(".", "")
battjsonsoc = str(sys.argv[3]).replace(".", "")

response = requests.get('http://'+battjsonurl, timeout=5)
response = json.loads(response)
speicherleistung = int(response[battjsonwatt])
with open("/var/www/html/openWB/ramdisk/speicherleistung", "w") as f:
    f.write(str(speicherleistung))

if battjsonsoc != "":
    battsoc = response[battjsonsoc]
else:
    battsoc = 0
with open("/var/www/html/openWB/ramdisk/speichersoc", "w") as f:
    f.write(str(battsoc))
