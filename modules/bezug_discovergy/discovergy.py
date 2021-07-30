#!/usr/bin/env python3

import json
import requests
import sys

username = str(sys.argv[1])
password = str(sys.argv[2])
id = str(sys.argv[3])

params = (
    ('meterId', id),
)

response = requests.get('https://api.discovergy.com/public/v1/last_reading', params=params, auth=(username, password), timeout = 3).json()

einspeisungwh = response["values"]["energyOut"] / 10000000
f = open('/var/www/html/openWB/ramdisk/einspeisungkwh', 'w')
f.write(str(einspeisungwh))
f.close()

bezugwh = response["values"]["energy"] / 10000000
f = open('/var/www/html/openWB/ramdisk/bezugkwh', 'w')
f.write(str(bezugwh))
f.close()

vl1=response["values"]["voltage1"] / 1000
f = open('/var/www/html/openWB/ramdisk/evuv1', 'w')
f.write(str(vl1))
f.close()
vl2=response["values"]["voltage2"] / 1000
f = open('/var/www/html/openWB/ramdisk/evuv2', 'w')
f.write(str(vl2))
f.close()
vl3=response["values"]["voltage3"] / 1000
f = open('/var/www/html/openWB/ramdisk/evuv3', 'w')
f.write(str(vl3))
f.close()

watt = response["values"]["power"] / 1000
f = open('/var/www/html/openWB/ramdisk/wattbezug', 'w')
f.write(str(watt))
f.close()
wattl1 = response["values"]["power1"] / 1000
f = open('/var/www/html/openWB/ramdisk/bezugw1', 'w')
f.write(str(wattl1))
f.close()
wattl2 = response["values"]["power2"] / 1000
f = open('/var/www/html/openWB/ramdisk/bezugw2', 'w')
f.write(str(wattl2))
f.close()
wattl3 = response["values"]["power3"] / 1000
f = open('/var/www/html/openWB/ramdisk/bezugw3', 'w')
f.write(str(wattl3))
f.close()
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