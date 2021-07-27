#!/usr/bin/env python3

import json
import requests
import sys

bezugjsonurl = str(sys.argv[1])
# Anpassen an alte Einstellungen
bezugjsonwatt = str(sys.argv[2]).replace(".", "")
bezugjsonkwh = str(sys.argv[3]).replace(".", "")
einspeisungjsonkwh = str(sys.argv[4]).replace(".", "")

response = requests.get("http://"+bezugjsonurl, timeout=5)
answer = json.loads(response)
evuwatt = int(answer[bezugjsonwatt])
with open("/var/www/html/openWB/ramdisk/wattbezug", "w") as f:
    f.write(str(evuwatt))

if bezugjsonkwh != "":
    evuikwh = answer[bezugjsonkwh]
else:
    evuikwh = 0
with open("/var/www/html/openWB/ramdisk/bezugkwh", "w") as f:
    f.write(str(evuikwh))

if einspeisungjsonkwh != "":
    evuekwh = answer[einspeisungjsonkwh]
else:
    evuekwh = 0
with open("/var/www/html/openWB/ramdisk/einspeisungkwh", "w") as f:
    f.write(str(evuekwh))
