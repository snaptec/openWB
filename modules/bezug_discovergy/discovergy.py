#!/usr/bin/env python3

import requests
import sys
import traceback

username = str(sys.argv[1])
password = str(sys.argv[2])
id = str(sys.argv[3])

def get_value(key, file, div):
    try:
        value = response["values"][key] / div
        f = open('/var/www/html/openWB/ramdisk/'+file, 'w')
        f.write(str(value))
        f.close()
        return value
    except:
        traceback.print_exc()

params = (
    ('meterId', id),
)

response = requests.get('https://api.discovergy.com/public/v1/last_reading', params=params, auth=(username, password), timeout = 3).json()

get_value("energyOut", "einspeisungkwh", 10000000)
get_value("energy", "bezugkwh", 10000000)

vl1=get_value("phase1Voltage", "evuv1", 1000)
vl2=get_value("phase2Voltage", "evuv2", 1000)
vl3=get_value("phase3Voltage", "evuv3", 1000)

get_value("power", "wattbezug", 1000)
wattl1=get_value("phase1Power", "bezugw1", 1000)
wattl2=get_value("phase2Power", "bezugw2", 1000)
wattl3=get_value("phase3Power", "bezugw3", 1000)

if vl1 > 150:
    al1 = wattl1 / vl1 
else:
    al1 = wattl1 / 230
if vl2 > 150:
    al2 = wattl2 / vl2
else:
    al2 = wattl2 / 230
if vl3 > 150:
    al3 = wattl3 / vl3
else:
    al3 = wattl3 / 230
f = open('/var/www/html/openWB/ramdisk/bezuga1', 'w')
f.write(str(al1))
f.close()
f = open('/var/www/html/openWB/ramdisk/bezuga2', 'w')
f.write(str(al2))
f.close()
f = open('/var/www/html/openWB/ramdisk/bezuga3', 'w')
f.write(str(al3))
f.close()