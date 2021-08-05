#!/usr/bin/env python3

import requests
import sys
import traceback

wrkostalpikoip = str(sys.argv[1])
speichermodul = str(sys.argv[2])
# Auslesen eines Kostal Piko WR über die integrierte API des WR mit angeschlossenem Eigenverbrauchssensor.

params = (
    ('dxsEntries', ['33556736', '251658753', '83887106', '83887362', '83887618)']),
)
pvwatttmp = requests.get('http://'+wrkostalpikoip+'/api/dxs.json', params=params, timeout=3).json()
# aktuelle Ausgangsleistung am WR [W]
try:
    pvwatt = int(pvwatttmp["dxsEntries"][0]["value"])
except:
    traceback.print_exc()

if pvwatt > 5:
    pvwatt = pvwatt*-1

# zur weiteren verwendung im webinterface
with open("/var/www/html/openWB/ramdisk/pvwatt", "w") as f:
    f.write(pvwatt)
# Gesamtzählerstand am WR [kWh]
try:
    pvkwh = int(pvwatttmp["dxsEntries"][1]["value"])
except:
    traceback.print_exc()
pvkwh = pvkwh*1000
# zur weiteren verwendung im webinterface
with open("/var/www/html/openWB/ramdisk/pvkwh", "w") as f:
    f.write(str(pvkwh))

try:
    bezugw1 = int(pvwatttmp["dxsEntries"][2]["value"])
except:
    traceback.print_exc()
try:
    bezugw2 = int(pvwatttmp["dxsEntries"][3]["value"])
except:
    traceback.print_exc()
try:
    bezugw3 = int(pvwatttmp["dxsEntries"][4]["value"])
except:
    traceback.print_exc()
if speichermodul == "speicher_bydhv":
    with open("/var/www/html/openWB/ramdisk/speicherleistung", "r") as f:
        speicherleistung = f.read()
    wattbezug = bezugw1+bezugw2+bezugw3+pvwatt+speicherleistung
else:
    wattbezug = bezugw1+bezugw2+bezugw3+pvwatt

with open("/var/www/html/openWB/ramdisk/wattbezug", "w") as f:
    f.write(str(wattbezug))
bezuga1 = round((bezugw1 / 225), 2)
bezuga2 = round((bezugw2 / 225), 2)
bezuga3 = round((bezugw3 / 225), 2)
with open("/var/www/html/openWB/ramdisk/bezuga1", "w") as f:
    f.write(str(bezuga1))
with open("/var/www/html/openWB/ramdisk/bezuga2", "w") as f:
    f.write(str(bezuga2))
with open("/var/www/html/openWB/ramdisk/bezuga3", "w") as f:
    f.write(str(bezuga3))
