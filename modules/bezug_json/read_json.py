#!/usr/bin/env python3

import requests
import sys
import traceback

bezugjsonurl = str(sys.argv[1])
# Anpassen an alte Einstellungen
bezugjsonwatt = str(sys.argv[2]).replace(".", "")
bezugjsonkwh = str(sys.argv[3]).replace(".", "")
einspeisungjsonkwh = str(sys.argv[4]).replace(".", "")

answer = requests.get(bezugjsonurl, timeout=5).json()
try:
    evuwatt = int(answer[bezugjsonwatt])
    with open("/var/www/html/openWB/ramdisk/wattbezug", "w") as f:
        f.write(str(evuwatt))
except:
    traceback.print_exc()

try:
    if bezugjsonkwh != "":
        evuikwh = answer[bezugjsonkwh]
    else:
        evuikwh = 0
    with open("/var/www/html/openWB/ramdisk/bezugkwh", "w") as f:
        f.write(str(evuikwh))
except:
    traceback.print_exc()

try:
    if einspeisungjsonkwh != "":
        evuekwh = answer[einspeisungjsonkwh]
    else:
        evuekwh = 0
    with open("/var/www/html/openWB/ramdisk/einspeisungkwh", "w") as f:
        f.write(str(evuekwh))
except:
    traceback.print_exc()
