#!/usr/bin/env python3

import json
import re
import requests
import sys

bezug_smartme_url = str(sys.argv[1])
bezug_smartme_user = str(sys.argv[2])
bezug_smartme_pass = str(sys.argv[3])

# Daten einlesen
response = requests.get('http://'+bezug_smartme_url, auth=(bezug_smartme_user, bezug_smartme_pass), timeout=10)
response = json.loads(response)

# Aktuelle Leistung (kW --> W)
wattbezug = response["ActivePower"]
wattbezug = int(wattbezug * 1000)

wattbezug1 = response["ActivePowerL1"]
wattbezug1 = int(wattbezug1 * 1000)

wattbezug2 = response["ActivePowerL2"]
wattbezug2 = int(wattbezug2 * 1000)

wattbezug3 = response["ActivePowerL3"]
wattbezug3 = int(wattbezug3 * 1000)

if wattbezug1 == 0:
    wattbezug1 = wattbezug

# Zählerstand Import(kWh)
ikwh = response["CounterReadingImport"]
ikwh = round(ikwh * 1000, 3)
# Zur Reduzierung der Datenmenge kann die folgende Zeile eingefügt werden.
# ikwh=$(echo "$ikwh / 1" | bc)

# Zählerstand Export(kWh)
ekwh = response["CounterReadingExport"]
ekwh = round(ekwh * 1000, 3)
# Zur Reduzierung der Datenmenge kann die folgende Zeile eingefügt werden.
# ekwh=$(echo "$ekwh / 1" | bc)

# Weitere Zählerdaten für die Statusseite (PowerFaktor, Spannung und Strom)
evupf1 = response["PowerFactorL1"]
evupf2 = response["PowerFactorL2"]
evupf3 = response["PowerFactorL3"]
evuv1 = response["VoltageL1"]
evuv2 = response["VoltageL2"]
evuv3 = response["VoltageL3"]
bezuga1 = response["CurrentL1"]
bezuga2 = response["CurrentL2"]
bezuga3 = response["CurrentL3"]
if bezuga1 == 'null':
    bezuga1 = response["Current"]

# Prüfen ob Werte gültig
regex = '^[-+]?[0-9]+\.?[0-9]*$'
if re.sreach(regex, wattbezug) == None:
    with open("/var/www/html/openWB/ramdisk/wattbezug", "r") as f:
        wattbezug = f.read()
if re.search(regex, ikwh) == None:
    with open("/var/www/html/openWB/ramdisk/bezugkwh", "r") as f:
        ikwh = f.read()
if re.search(regex, ekwh) == None:
    with open("/var/www/html/openWB/ramdisk/einspeisungkwh", "r") as f:
        ekwh = f.read()

# Ausgabe
with open("/var/www/html/openWB/ramdisk/wattbezug", "w") as f:
    f.write(str(wattbezug))
with open("/var/www/html/openWB/ramdisk/bezugw1", "w") as f:
    f.write(str(wattbezug1))
with open("/var/www/html/openWB/ramdisk/bezugw2", "w") as f:
    f.write(str(wattbezug2))
with open("/var/www/html/openWB/ramdisk/bezugw3", "w") as f:
    f.write(str(wattbezug3))
with open("/var/www/html/openWB/ramdisk/bezugkwh", "w") as f:
    f.write(str(ikwh))
with open("/var/www/html/openWB/ramdisk/einspeisungkwh", "w") as f:
    f.write(str(ekwh))
with open("/var/www/html/openWB/ramdisk/evupf1", "w") as f:
    f.write(str(evupf1))
with open("/var/www/html/openWB/ramdisk/evupf2", "w") as f:
    f.write(str(evupf2))
with open("/var/www/html/openWB/ramdisk/evupf3", "w") as f:
    f.write(str(evupf3))
with open("/var/www/html/openWB/ramdisk/evuv1", "w") as f:
    f.write(str(evuv1))
with open("/var/www/html/openWB/ramdisk/evuv2", "w") as f:
    f.write(str(evuv2))
with open("/var/www/html/openWB/ramdisk/evuv3", "w") as f:
    f.write(str(evuv3))
with open("/var/www/html/openWB/ramdisk/bezuga1", "w") as f:
    f.write(str(bezuga1))
with open("/var/www/html/openWB/ramdisk/bezuga2", "w") as f:
    f.write(str(bezuga2))
with open("/var/www/html/openWB/ramdisk/bezuga3", "w") as f:
    f.write(str(bezuga3))
