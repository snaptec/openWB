#!/usr/bin/env python3

import requests
import sys
import traceback

powerfoxid = str(sys.argv[1])
powerfoxuser = str(sys.argv[2])
powerfoxpass = str(sys.argv[3])

response = requests.get('https://backend.powerfox.energy/api/2.0/my/'+powerfoxid+'/current', auth=(powerfoxuser, powerfoxpass), timeout=3).json()
try:
    einspeisungwh = response['A_Minus']
    with open("/var/www/html/openWB/ramdisk/einspeisungkwh", "w") as f:
        f.write(str(einspeisungwh))
except:
    traceback.print_exc()

try:
    bezugwh = response['A_Plus']
    with open("/var/www/html/openWB/ramdisk/bezugkwh", "w") as f:
        f.write(str(bezugwh))
except:
    traceback.print_exc()

try:
    watt = response['Watt']
    with open("/var/www/html/openWB/ramdisk/wattbezug", "w") as f:
        f.write(str(watt))
except:
    traceback.print_exc()
