#!/usr/bin/env python3

from datetime import datetime, timezone
import os
import re
import requests
import sys
import traceback

Debug = int(os.environ.get('debug'))
myPid = str(os.getpid())

sonnenecoalternativ = str(sys.argv[1])
sonnenecoip = str(sys.argv[2])

def DebugLog(message: str) -> None:
    local_time = datetime.now(timezone.utc).astimezone()
    print(local_time.strftime(format="%Y-%m-%d %H:%M:%S") + ": PID: " + myPid + ": " + message)


if Debug >= 2:
    DebugLog('Speicher Alternativ: ' + sonnenecoalternativ)
    DebugLog('Speicher IP: ' + sonnenecoip)

ra = '^-?[0-9]+$'

def check_write_value(valueString: str, file: str, fallback: str = "0") -> None:
    if re.search(ra, valueString) == None:
        DebugLog('invalid valueString: ' + valueString + ' setting fallback of \'' + fallback + '\'')
        valueString = fallback
    if Debug >= 1:
        DebugLog(file+': ' + valueString)
    with open("/var/www/html/openWB/ramdisk/" + file, "w") as f:
        f.write(valueString)


# Auslesen einer Sonnbenbatterie Eco 4.5 über die integrierte JSON-API des Batteriesystems
if sonnenecoalternativ == 2:
    baseurl = 'http://' + sonnenecoip + ':7979/rest/devices/battery/'
    response = requests.get(baseurl + 'M05', timeout=5)
    response.encoding = 'utf-8'
    speichersoc = response.text.replace("\n", "")
    speichersoc = int(speichersoc)
    response = requests.get(baseurl + 'M01', timeout=5)
    response.encoding = 'utf-8'
    speicherentladung = response.text.replace("\n", "")
    response = requests.get(baseurl + 'M02', timeout=5)
    response.encoding = 'utf-8'
    speicherladung = response.text.replace("\n", "")
    speicherladung = int(speicherladung)
    speicherentladung = int(speicherentladung)
    speicherwatt = speicherladung - speicherentladung
    # wenn Batterie aus bzw. keine Antwort ersetze leeren Wert durch eine 0
    check_write_value(str(speicherwatt), "speicherleistung")
    check_write_value(str(speichersoc), "speichersoc")
    response = requests.get(baseurl + 'M03', timeout=5)
    response.encoding = 'utf-8'
    pvwatt = response.text.replace("\n", "")
    pvwatt = int(pvwatt)
    pvwatt = pvwatt * -1
    if Debug >= 1:
        DebugLog('PV Leistung: ' + str(pvwatt))
    check_write_value(str(pvwatt), "pvwatt")

else:
    if sonnenecoalternativ == 0:
        speicherantwort = requests.get('http://' + sonnenecoip + ':7979/rest/devices/battery', timeout=5).json()
        try:
            speichersoc = int(speicherantwort["M05"])
        except:
            traceback.print_exc()
            exit(1)
        try:
            speicherentladung = int(speicherantwort["M34"])
        except:
            traceback.print_exc()
            exit(1)
        try:
            speicherladung = int(speicherantwort["M35"])
        except:
            traceback.print_exc()
            exit(1)
        speicherwatt = speicherladung - speicherentladung
        # wenn Batterie aus bzw. keine Antwort ersetze leeren Wert durch eine 0
        check_write_value(str(speicherwatt), "speicherleistung")
        check_write_value(str(speichersoc), "speichersoc")
    else:
        speicherantwort = requests.get("http://" + sonnenecoip + "/api/v1/status", timeout=5).json()
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
            speicherwatt = speicherantwort["Pac_total_W"]
        except:
            traceback.print_exc()
            exit(1)
        try:
            speichersoc = speicherantwort["USOC"]
            if Debug >= 1:
                DebugLog('SpeicherSoC: ' + str(speichersoc))
            check_write_value(str(speichersoc), "speichersoc")
        except:
            traceback.print_exc()
            exit(1)
        try:
            speicherpvwatt = speicherantwort["Production_W"]
        except:
            traceback.print_exc()
            exit(1)
        speicherpvwatt = speicherpvwatt * -1
        if Debug >= 1:
            DebugLog('Speicher PV Watt: ' + str(speicherpvwatt))
        check_write_value(str(speicherpvwatt), "pvwatt")
        if re.search(ra, str(speicherwatt)) != None:
            speicherwatt = speicherwatt * -1
        if Debug >= 1:
            DebugLog('Speicherleistung: ' + str(speicherwatt))
        check_write_value(str(speicherwatt), "speicherleistung")

exit(0)
