#!/usr/bin/env python3
from datetime import datetime, timezone
import os
import requests
import sys
import traceback

sonnenecoalternativ = int(sys.argv[1])
sonnenecoip = str(sys.argv[2])

Debug = int(os.environ.get('debug'))
myPid = str(os.getpid())


def DebugLog(message):
    local_time = datetime.now(timezone.utc).astimezone()
    print(local_time.strftime(format="%Y-%m-%d %H:%M:%S") + ": PID: " + myPid + ": " + message)


if Debug >= 2:
    DebugLog('Sonneneco Alternativ: ' + sonnenecoalternativ)
    DebugLog('Sonneneco IP: ' + sonnenecoip)

# Auslesen einer Sonnbenbatterie Eco 4.5 über die integrierte JSON-API des Batteriesystems
if sonnenecoalternativ == 2:
    evu_bezug = int(requests.get('http://' + sonnenecoip + ':7979/rest/devices/battery/M39', timeout=5).text)
    evu_einspeisung = int(requests.get('http://' + sonnenecoip + ':7979/rest/devices/battery/M38', timeout=5).text)
    wattbezug = evu_bezug - evu_einspeisung

    with open("/var/www/html/openWB/ramdisk/wattbezug", "w") as f:
        f.write(str(wattbezug))
else:
    if sonnenecoalternativ == 1:
        speicherantwort = requests.get("http://"+sonnenecoip+"/api/v1/status", timeout=5).json()
        try:
            wattbezug = speicherantwort["GridFeedIn_W"]
        except:
            traceback.print_exc()
            exit(1)
        # Negativ ist Verbrauch, positiv Einspeisung
        wattbezug = wattbezug * -1
        # Es wird nur eine Spannung ausgegeben
        try:
            evuv1 = speicherantwort["Uac"]
        except:
            traceback.print_exc()
            exit(1)
        evuv2 = evuv1
        evuv3 = evuv1
        try:
            evuhz = speicherantwort["Fac"]
        except:
            traceback.print_exc()
            exit(1)
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
        exit(1)

    # Schreibe alle Werte in die Ramdisk.
    if Debug >= 1:
        DebugLog('Leistung: ' + str(wattbezug))
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
    if Debug >= 1:
        DebugLog('Import: ' + str(ikwh))
    with open("/var/www/html/openWB/ramdisk/bezugkwh", "w") as f:
        f.write(str(ikwh))
    if Debug >= 1:
        DebugLog('Export: ' + str(ekwh))
    with open("/var/www/html/openWB/ramdisk/einspeisungkwh", "w") as f:
        f.write(str(ekwh))

exit(0)
