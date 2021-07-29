#!/usr/bin/env python3

import json
import re
import requests
import sys

sonnenecoalternativ = str(sys.argv[1])
sonnenecoip = str(sys.argv[2])

ra = '^-?[0-9]+$'

def check_write_value(value, file):
    global ra 
    if re.search(ra, value) == None:
        value = "0"
    with open("/var/www/html/openWB/ramdisk/"+file, "w") as f:
        f.write(str(value))


# Auslesen einer Sonnbenbatterie Eco 4.5 über die integrierte JSON-API des Batteriesystems
if sonnenecoalternativ == 2:
    speichersoc = requests.get('http://'+sonnenecoip+':7979/rest/devices/battery/M05', timeout=5)
    speichersoc = int(speichersoc)
    speicherentladung = requests.get('http://'+sonnenecoip+':7979/rest/devices/battery/M01', timeout=5)
    speicherladung = requests.get('http://'+sonnenecoip+':7979/rest/devices/battery/M02', timeout=5)
    speicherladung = int(speicherladung)
    speicherentladung = int(speicherentladung)
    speicherwatt = speicherladung - speicherentladung
    # wenn Batterie aus bzw. keine Antwort ersetze leeren Wert durch eine 0
    check_write_value(speicherwatt, "speicherleistung")
    check_write_value(speichersoc, "speichersoc")
    pvwatt = requests.get('http://'+sonnenecoip+':7979/rest/devices/battery/M03', timeout=5)
    pvwatt = int(pvwatt)
    pvwatt = pvwatt * -1
    with open("/var/www/html/openWB/ramdisk/pvwatt", "w") as f:
        f.write(str(pvwatt))
else:
    if sonnenecoalternativ == 0:
        speicherantwort = requests.get('http://'+sonnenecoip+':7979/rest/devices/battery', timeout=5)
        speicherantwort = json.loads(speicherantwort)
        speichersoc = int(speicherantwort["M05"])
        speicherentladung = int(speicherantwort["M34"])
        speicherladung = int(speicherantwort["M35"])
        speicherwatt = speicherladung - speicherentladung
        # wenn Batterie aus bzw. keine Antwort ersetze leeren Wert durch eine 0
        check_write_value(speicherwatt, "speicherleistung")
        check_write_value(speichersoc, "speichersoc")
    else:
        speicherantwort = requests.get("http://"+sonnenecoip+"/api/v1/status", timeout=5)
        speicherantwort = json.loads(speicherantwort)
        speicherwatt = speicherantwort["Pac_total_W"]
        speichersoc = speicherantwort["USOC"]
        speicherpvwatt = speicherantwort["Production_W"]
        speicherpvwatt = speicherpvwatt * -1
        with open("/var/www/html/openWB/ramdisk/pvwatt", "w") as f:
            f.write(str(speicherpvwatt))
        if re.search(ra, speicherwatt) == None:
            speicherwatt = "0"
        else:
            speicherwatt = speicherwatt * -1
        with open("/var/www/html/openWB/ramdisk/speicherleistung", "w") as f:
            f.write(str(speicherwatt))
        check_write_value(speichersoc, "speichersoc")
