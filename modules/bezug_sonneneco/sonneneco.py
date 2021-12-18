#!/usr/bin/env python3
from datetime import datetime, timezone
import os
import re
import requests
import sys
import traceback

sonnenecoalternativ = int(sys.argv[1])
sonnenecoip = str(sys.argv[2])

Debug = int(os.environ.get('debug'))
myPid = str(os.getpid())


def DebugLog(message: str) -> None:
    local_time = datetime.now(timezone.utc).astimezone()
    print(local_time.strftime(format="%Y-%m-%d %H:%M:%S") + ": PID: " + myPid + ": " + message)


ra = '^-?[0-9]+(.[0-9]+)?$'  # re for valid float as str


def check_write_value(valueString: str, file: str, fallback: str = "0") -> None:
    if re.search(ra, valueString) == None:
        DebugLog('invalid valueString: ' + valueString + ' setting fallback of \'' + fallback + '\'')
        valueString = fallback
    if Debug >= 1:
        DebugLog(file+': ' + valueString)
    with open("/var/www/html/openWB/ramdisk/" + file, "w") as f:
        f.write(valueString)


if Debug >= 2:
    DebugLog('Sonneneco Alternativ: ' + str(sonnenecoalternativ))
    DebugLog('Sonneneco IP: ' + sonnenecoip)

# Auslesen einer Sonnbenbatterie Eco 4.5 über die integrierte JSON-API des Batteriesystems
if sonnenecoalternativ == 2:
    baseurl = 'http://' + sonnenecoip + ':7979/rest/devices/battery/'
    evu_bezug = int(requests.get(baseurl + 'M39', timeout=5).text)
    evu_einspeisung = int(requests.get(baseurl + 'M38', timeout=5).text)
    wattbezug = evu_bezug - evu_einspeisung
    check_write_value(str(wattbezug), "wattbezug")
else:
    if sonnenecoalternativ == 1:
        speicherantwort = requests.get("http://"+sonnenecoip+"/api/v1/status", timeout=5).json()
        '''
        example data:
        {
            "Apparent_output": 225,
            "BackupBuffer": "0",
            "BatteryCharging": false,
            "BatteryDischarging": false,
            "Consumption_Avg": 2114,
            "Consumption_W": 2101,
            "Fac": 49.97200393676758,
            "FlowConsumptionBattery": false,
            "FlowConsumptionGrid": true,
            "FlowConsumptionProduction": false,
            "FlowGridBattery": false,
            "FlowProductionBattery": false,
            "FlowProductionGrid": false,
            "GridFeedIn_W": -2106,
            "IsSystemInstalled": 1,
            "OperatingMode": "2",
            "Pac_total_W": -5,
            "Production_W": 0,
            "RSOC": 6,
            "RemainingCapacity_Wh": 2377,
            "Sac1": 75,
            "Sac2": 75,
            "Sac3": 75,
            "SystemStatus": "OnGrid",
            "Timestamp": "2021-12-13 07:54:48",
            "USOC": 0,
            "Uac": 231,
            "Ubat": 48,
            "dischargeNotAllowed": true,
            "generator_autostart": false,
            "NVM_REINIT_STATUS": 0
        }
        '''
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
        DebugLog('Import: ' + str(ikwh))
        DebugLog('Export: ' + str(ekwh))
    check_write_value(str(wattbezug), "wattbezug")
    check_write_value(str(evuv1), "evuv1")
    check_write_value(str(evuv2), "evuv2")
    check_write_value(str(evuv3), "evuv3")
    check_write_value(str(bezugw1), "bezugw1")
    check_write_value(str(bezugw2), "bezugw2")
    check_write_value(str(bezugw3), "bezugw3")
    check_write_value(str(bezuga1), "bezuga1")
    check_write_value(str(bezuga2), "bezuga2")
    check_write_value(str(bezuga3), "bezuga3")
    check_write_value(str(evuhz), "evuhz")
    check_write_value(str(evupf1), "evupf1")
    check_write_value(str(evupf2), "evupf2")
    check_write_value(str(evupf3), "evupf3")
    check_write_value(str(ikwh), "bezugkwh")
    check_write_value(str(ekwh), "einspeisungkwh")

exit(0)
