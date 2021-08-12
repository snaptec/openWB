#!/usr/bin/env python3

import requests
import sys
import traceback

sonnenecoalternativ = int(sys.argv[1])
sonnenecoip = str(sys.argv[2])

# Auslesen einer Sonnbenbatterie Eco 4.5 über die integrierte JSON-API des Batteriesystems
if sonnenecoalternativ == 2:
    response = requests.get('http://'+sonnenecoip+':7979/rest/devices/battery/M39', timeout=5)
    response.encoding = 'utf-8'
    evubezug = response.text.replace("\n", "")
    response = requests.get('http://'+sonnenecoip+':7979/rest/devices/battery/M38', timeout=5)
    response.encoding = 'utf-8'
    evueinspeisung = response.text.replace("\n", "")
    evubezug = int(evubezug)
    evueinspeisung = int(evueinspeisung)
    wattbezug = evubezug - evueinspeisung

    with open("/var/www/html/openWB/ramdisk/wattbezug", "w") as f:
        f.write(str(wattbezug))
else:
    if sonnenecoalternativ == 1:
        speicherantwort = requests.get("http://"+sonnenecoip+"/api/v1/status", timeout=5).json()
        try:
            wattbezug = speicherantwort["GridFeedIn_W"]
        except:
            traceback.print_exc()
        # Negativ ist Verbrauch, positiv Einspeisung
        wattbezug = wattbezug * -1
        # Es wird nur eine Spannung ausgegeben
        try:
            evuv1 = speicherantwort["Uac"]
        except:
            traceback.print_exc()
        evuv2 = evuv1
        evuv3 = evuv1
        try:
            evuhz = speicherantwort["Fac"]
        except:
            traceback.print_exc()
        # Weitere Daten müssen errechnet werden
        # Es wird angenommen, dass alle Phasen gleich ausgelastet sind
        bezugw1 = round((wattbezug / 3), 2)
        bezugw2 = bezugw1
        bezugw3 = bezugw1
        bezuga1 = round((bezugw1 / evuv1), 2)
        bezuga2 = bezuga1
        bezuga3 = bezuga1
        # Weitere Daten können nicht ermittelt werden
        evupf1 = 1
        evupf2 = 1
        evupf3 = 1
        ikwh = 0
        ekwh = 0
    else:
        # Bietet die Rest API die Daten?
        sys.exit(0)

    # Schreibe alle Werte in die Ramdisk.
    with open("/var/www/html/openWB/ramdisk/wattbezug", "w") as f:
        f.write(str(wattbezug))
    with open("/var/www/html/openWB/ramdisk/evuv1", "w") as f:
        f.write(str(evuv1))
    with open("/var/www/html/openWB/ramdisk/evuv2", "w") as f:
        f.write(str(evuv2))
    with open("/var/www/html/openWB/ramdisk/evuv3", "w") as f:
        f.write(str(evuv3))
    with open("/var/www/html/openWB/ramdisk/bezugw1", "w") as f:
        f.write(str(bezugw1))
    with open("/var/www/html/openWB/ramdisk/bezugw2", "w") as f:
        f.write(str(bezugw2))
    with open("/var/www/html/openWB/ramdisk/bezugw3", "w") as f:
        f.write(str(bezugw3))
    with open("/var/www/html/openWB/ramdisk/bezuga1", "w") as f:
        f.write(str(bezuga1))
    with open("/var/www/html/openWB/ramdisk/bezuga2", "w") as f:
        f.write(str(bezuga2))
    with open("/var/www/html/openWB/ramdisk/bezuga3", "w") as f:
        f.write(str(bezuga3))
    with open("/var/www/html/openWB/ramdisk/evuhz", "w") as f:
        f.write(str(evuhz))
    with open("/var/www/html/openWB/ramdisk/evupf1", "w") as f:
        f.write(str(evupf1))
    with open("/var/www/html/openWB/ramdisk/evupf2", "w") as f:
        f.write(str(evupf2))
    with open("/var/www/html/openWB/ramdisk/evupf3", "w") as f:
        f.write(str(evupf3))
    with open("/var/www/html/openWB/ramdisk/bezugkwh", "w") as f:
        f.write(str(ikwh))
    with open("/var/www/html/openWB/ramdisk/einspeisungkwh", "w") as f:
        f.write(str(ekwh))
