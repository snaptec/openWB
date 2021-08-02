#!/usr/bin/env python3

import requests
import sys

wrkostalpikoip = str(sys.argv[1])
speichermodul = str(sys.argv[2])
# Auslesen eines Kostal Piko WR über die integrierte API des WR mit angeschlossenem Eigenverbrauchssensor.

params = (
    ('dxsEntries', ['33556736', '251658753', '83887106', '83887362', '83887618)']),
)
pvwatttmp = requests.get('http://'+wrkostalpikoip+'/api/dxs.json', params=params, timeout=3).json()
# aktuelle Ausgangsleistung am WR [W]
pvwatt = int(pvwatttmp["dxsEntries"][0]["value"])

if pvwatt > 5:
    pvwatt = pvwatt*-1

# zur weiteren verwendung im webinterface
with open("/var/www/html/openWB/ramdisk/pvwatt", "w") as f:
    f.write(pvwatt)
# Gesamtzählerstand am WR [kWh]
pvkwh = int(pvwatttmp["dxsEntries"][1]["value"])
pvkwh = pvkwh*1000
# zur weiteren verwendung im webinterface
with open("/var/www/html/openWB/ramdisk/pvkwh", "w") as f:
    f.write(str(pvkwh))

bezugw1 = int(pvwatttmp["dxsEntries"][2]["value"])
bezugw2 = int(pvwatttmp["dxsEntries"][3]["value"])
bezugw3 = int(pvwatttmp["dxsEntries"][4]["value"])
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
