#!/usr/bin/env python3

import json
import re
import requests
import sys

wryoulessip = str(sys.argv[1])
wryoulessalt = str(sys.argv[2])

# Auslesen vom S0-Eingang eines Youless LS120 Energy Monitor.
params = (('f', 'j'),)
response = requests.get(wryoulessip+'/a', params=params, timeout=5)
answer = response.json()
if wryoulessalt == 0:
    # aktuelle Ausgangsleistung am WR [W]
    pvwatt = int(answer["ps0"])
    # Gesamtz‰hlerstand am WR [Wh]
    pvkwh = answer["cs0"]
    pvkwh = pvkwh.replace(",", "")
else:
    # aktuelle Ausgangsleistung am WR [W]
    pvwatt = int(answer["pwr"])
    # Gesamtz‰hlerstand am WR [Wh]
    pvkwh = answer["cnt"]
    pvkwh = pvkwh.replace(",", "")

if pvwatt > 5:
    pvwatt = pvwatt*-1
with open("/var/www/html/openWB/ramdisk/pvwatt", "w") as f:
    f.write(str(pvwatt))
with open("/var/www/html/openWB/ramdisk/pvkwh", "w") as f:
    f.write(str(pvkwh))
# Gesamtzählerstand am WR [kWh]
pvkwh = pvkwh/1000
with open("/var/www/html/openWB/ramdisk/pvkwhk", "w") as f:
    f.write(str(pvkwh))
