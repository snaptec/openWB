#!/usr/bin/env python3

import json
import requests
import sys
import traceback

bezug_solarlog_ip = str(sys.argv[1])
bezug_solarlog_speicherv = str(sys.argv[1])

data = {"801": {"170": None}}
data = json.dumps(data)
response = requests.post('http://'+bezug_solarlog_ip+'/getjp', data=data, timeout=5).json()

try:
    pvwatt = response["801"]["170"]["101"]
except:
    traceback.print_exc()
try:
    hausverbrauch = response["801"]["170"]["110"]
except:
    traceback.print_exc()
bezugwatt = hausverbrauch - pvwatt
try:
    pvkwh = response["801"]["170"]["109"]
except:
    traceback.print_exc()

if bezug_solarlog_speicherv == 1:
    with open("ramdisk/speicherleistung", "r") as f:
        speicherleistung = f.read()
    bezugwatt = bezugwatt + speicherleistung
if pvwatt > 5:
    pvwatt = pvwatt*-1

with open("/var/www/html/openWB/ramdisk/wattbezug", "w") as f:
    f.write(str(bezugwatt))
with open("/var/www/html/openWB/ramdisk/pvwatt", "w") as f:
    f.write(str(pvwatt))
with open("/var/www/html/openWB/ramdisk/pvkwh", "w") as f:
    f.write(str(pvkwh))
pvkwhk = pvkwh*1000
with open("/var/www/html/openWB/ramdisk/pvkwhk", "w") as f:
    f.write(str(pvkwhk))
