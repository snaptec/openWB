#!/usr/bin/env python3

import json
import requests
import sys

bezug_solarlog_ip = str(sys.argv[1])
bezug_solarlog_speicherv = str(sys.argv[1])

data = {"801": {"170": None}}
data = json.dumps(data)
response = requests.post('http://'+bezug_solarlog_ip+'/getjp', data=data, timeout=5).json()


pvwatt = response["801"]["170"]["101"]
hausverbrauch = response["801"]["170"]["110"]
bezugwatt = hausverbrauch - pvwatt
pvkwh = response["801"]["170"]["109"]

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
