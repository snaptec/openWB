#!/usr/bin/env python3
from datetime import datetime, timezone
import os
import re
import requests
import sys
import traceback

froniusvar2 = str(sys.argv[1])
froniuserzeugung = str(sys.argv[2])
wrfroniusip = str(sys.argv[3])
froniusmeterlocation = str(sys.argv[4])

Debug = int(os.environ.get('debug'))
myPid = str(os.getpid())


def DebugLog(level, message):
    if Debug >= level:
        local_time = datetime.now(timezone.utc).astimezone()
        print(local_time.strftime(format="%Y-%m-%d %H:%M:%S") + ": PID: " + myPid + ": " + message)


def get_rounded_value(response, key):
    try:
        value = round(response[key], 2)
        return value
    except:
        traceback.print_exc()
        exit(1)


def get_int_value(response, key):
    try:
        value = int(response[key])
        return value
    except:
        traceback.print_exc()
        exit(1)


DebugLog(2, 'Fronius SM Variante: ' + froniusvar2)
DebugLog(2, 'Fronius SM Erzeugung: ' + froniuserzeugung)
DebugLog(2, 'Fronius SM IP: ' + wrfroniusip)
DebugLog(2, 'Fronius SM Zaehlerort: ' + froniusmeterlocation)

# Auslesen eines Fronius Symo WR mit Fronius Smartmeter über die integrierte JSON-API des WR.
# Rückgabewert ist die aktuelle Einspeiseleistung (negativ) oder Bezugsleistung (positiv).
# Einspeiseleistung: PV-Leistung > Verbrauch, es wird Strom eingespeist
# Bezugsleistug: PV-Leistung < Verbrauch, es wird Strom aus dem Netz bezogen

# Fordere die Werte vom SmartMeter an.
if froniusvar2 == "0":
    # Hole die JSON Daten
    params = (
        ('Scope', 'Device'),
        ('DeviceId', froniuserzeugung),
    )
    response_sm = requests.get('http://'+wrfroniusip+'/solar_api/v1/GetMeterRealtimeData.cgi', params=params, timeout=5)
    response = response_sm.json()
    DebugLog(1, 'response_sm: ' + str(response_sm))
    DebugLog(2, 'response_sm_data: ' + str(response))

    # Setze die für JSON Abruf benötigte DeviceID
    try:
        response_json_id = response["Body"]["Data"]
    except:
        traceback.print_exc()
        exit(1)

elif froniusvar2 == "1":
    # Hole die JSON-Daten
    params = (
        ('Scope', 'System'),
    )
    response_sm = requests.get('http://'+wrfroniusip+'/solar_api/v1/GetMeterRealtimeData.cgi', params=params, timeout=5)
    response = response_sm.json()
    DebugLog(1, 'response_sm: ' + str(response_sm))
    DebugLog(2, 'response_sm_data: ' + str(response))

    # Setze die für JSON Abruf benötigte DeviceID
    try:
        response_json_id = response["Body"]["Data"][froniuserzeugung]
    except:
        traceback.print_exc()
        exit(1)
    # TODO: Evtl. ist es noch weiter zu vereinfachen -> selbe response_sm wie in Variante0 mit folgendem Aufruf:
    # response_sm=$(curl --connect-timeout 5 -s "$wrfroniusip/solar_api/v1/GetMeterRealtimeData.cgi?Scope=Device&DeviceID=$froniuserzeugung&DataCollection=MeterRealtimeData")
    # dann auch json_id wieder gleich:
    # json_id=".Body.Data"

elif froniusvar2 == "2":
    # Hole die JSON-Daten
    params = (
        ('Scope', 'System'),
    )
    response_sm = requests.get('http://'+wrfroniusip+'/solar_api/v1/GetMeterRealtimeData.cgi', params=params, timeout=5)
    response = response_sm.json()
    DebugLog(1, 'response_sm: ' + str(response_sm))
    DebugLog(2, 'response_sm_data: ' + str(response))

    # Setze die für JSON Abruf benötigte DeviceID
    try:
        response_json_id = response["Body"]["Data"][froniuserzeugung]
    except:
        traceback.print_exc()
        exit(1)
    # TODO: meter_location für diese Variante korrekt ermitteln
    # Überprüfe den Einbauort des SmartMeters.
    meter_location = froniusmeterlocation

    # Lese alle wichtigen Werte aus der JSON-Antwort und skaliere sie gleich.
    wattbezug = get_int_value(response_json_id, "SMARTMETER_POWERACTIVE_MEAN_SUM_F64")
    evuv1 = get_rounded_value(response_json_id, "SMARTMETER_VOLTAGE_01_F64")
    evuv2 = get_rounded_value(response_json_id, "SMARTMETER_VOLTAGE_02_F64")
    evuv3 = get_rounded_value(response_json_id, "SMARTMETER_VOLTAGE_03_F64")
    bezugw1 = get_rounded_value(response_json_id, "SMARTMETER_POWERACTIVE_MEAN_01_F64")
    bezugw2 = get_rounded_value(response_json_id, "SMARTMETER_POWERACTIVE_MEAN_02_F64")
    bezugw3 = get_rounded_value(response_json_id, "SMARTMETER_POWERACTIVE_MEAN_03_F64")
    # Berechne den Strom und lese ihn nicht direkt (der eigentlich zu lesende direkte Wert
    # "Current_AC_Phase_1" wäre der Absolutwert und man würde das Vorzeichen verlieren).
    bezuga1 = round(bezugw1 / evuv1, 2)
    bezuga2 = round(bezugw2 / evuv2, 2)
    bezuga3 = round(bezugw3 / evuv3, 2)
    evuhz = get_rounded_value(response_json_id, "GRID_FREQUENCY_MEAN_F32")
    evupf1 = get_rounded_value(response_json_id, "SMARTMETER_FACTOR_POWER_01_F64")
    evupf2 = get_rounded_value(response_json_id, "SMARTMETER_FACTOR_POWER_02_F64")
    evupf3 = get_rounded_value(response_json_id, "SMARTMETER_FACTOR_POWER_03_F64")
    try:
        ikwh = response_json_id["SMARTMETER_ENERGYACTIVE_CONSUMED_SUM_F64"]
    except:
        traceback.print_exc()
        exit(1)
    try:
        ekwh = response_json_id["SMARTMETER_ENERGYACTIVE_PRODUCED_SUM_F64"]
    except:
        traceback.print_exc()
        exit(1)

# Auswertung für Variante0 und Variante1 gebündelt
if froniusvar2 != "2":
    # Überprüfe den Einbauort des SmartMeters.
    try:
        meter_location = str(response_json_id["Meter_Location_Current"])
    except:
        traceback.print_exc()
        exit(1)
    DebugLog(1, 'Zaehlerort: ' + str(meter_location))

    # Lese alle wichtigen Werte aus der JSON-Antwort und skaliere sie gleich.
    wattbezug = get_int_value(response_json_id, "PowerReal_P_Sum")
    evuv1 = get_rounded_value(response_json_id, "Voltage_AC_Phase_1")
    evuv2 = get_rounded_value(response_json_id, "Voltage_AC_Phase_2")
    evuv3 = get_rounded_value(response_json_id, "Voltage_AC_Phase_3")
    bezugw1 = get_rounded_value(response_json_id, "PowerReal_P_Phase_1")
    bezugw2 = get_rounded_value(response_json_id, "PowerReal_P_Phase_2")
    bezugw3 = get_rounded_value(response_json_id, "PowerReal_P_Phase_3")
    # Berechne den Strom und lese ihn nicht direkt (der eigentlich zu lesende direkte Wert
    # "Current_AC_Phase_1" wäre der Absolutwert und man würde das Vorzeichen verlieren).
    bezuga1 = round(bezugw1 / evuv1, 2)
    bezuga2 = round(bezugw2 / evuv2, 2)
    bezuga3 = round(bezugw3 / evuv3, 2)
    evuhz = get_rounded_value(response_json_id, "Frequency_Phase_Average")
    evupf1 = get_rounded_value(response_json_id, "PowerFactor_Phase_1")
    evupf2 = get_rounded_value(response_json_id, "PowerFactor_Phase_2")
    evupf3 = get_rounded_value(response_json_id, "PowerFactor_Phase_3")
    try:
        ikwh = response_json_id["EnergyReal_WAC_Sum_Consumed"]
    except:
        traceback.print_exc()
        exit(1)
    try:
        ekwh = response_json_id["EnergyReal_WAC_Sum_Produced"]
    except:
        traceback.print_exc()
        exit(1)

if meter_location == "1":
    # wenn SmartMeter im Verbrauchszweig sitzt sind folgende Annahmen getroffen:
    # PV Leistung wird gleichmäßig auf alle Phasen verteilt
    # Spannungen und Leistungsfaktoren sind am Verbrauchszweig == Einspeisepunkt

    # Lese die aktuelle PV-Leistung des Wechselrichters ein.
    params = (
        ('Scope', 'System'),
    )
    response_fi = requests.get('http://'+wrfroniusip+'/solar_api/v1/GetPowerFlowRealtimeData.fcgi', params=params, timeout=3)
    response = response_fi.json()
    DebugLog(1, 'response_fi: ' + str(response_fi))
    DebugLog(2, 'response_fi_data: ' + str(response))

    # Basis ist die Leistungsangabe aus dem WR!
    try:
        wattbezug = int(response["Body"]["Data"]["Site"]["P_Grid"])
    except:
        traceback.print_exc()
        exit(1)
    try:
        pvwatt = response["Body"]["Data"]["Site"]["P_PV"]
    except:
        traceback.print_exc()
        exit(1)
    # Wenn WR aus bzw. im Standby (keine Antwort), ersetze leeren Wert durch eine 0.
    regex = '^-?[0-9]+$'
    if re.search(regex, str(pvwatt)) == None:
        pvwatt = 0
    # Hier gehen wir mal davon aus, dass der Wechselrichter seine PV-Leistung gleichmäßig auf alle Phasen aufteilt.
    bezugw1 = round((-1 * bezugw1 - pvwatt/3), 2)
    bezugw2 = round((-1 * bezugw2 - pvwatt/3), 2)
    bezugw3 = round((-1 * bezugw3 - pvwatt/3), 2)
    # Wegen der geänderten Leistungen sind die Ströme erneut zu berechnen
    bezuga1 = round((bezugw1 / evuv1), 2)
    bezuga2 = round((bezugw2 / evuv2), 2)
    bezuga3 = round((bezugw3 / evuv3), 2)
    # Beim Energiebezug ist nicht klar, welcher Anteil aus dem Netz bezogen wurde, und was aus dem Wechselrichter kam.
    # ikwh=$(echo $response_sm | jq '.Body.Data.EnergyReal_WAC_Sum_Consumed')
    ikwh = 0
    # Beim Energieexport ist nicht klar, wie hoch der Eigenverbrauch während der Produktion war.
    # ekwh=$(echo $response_fi | jq '.Body.Data.Site.E_Total')
    ekwh = 0
    with open("/var/www/html/openWB/ramdisk/fronius_sm_bezug_meterlocation", "w") as f:
        f.write(str(1))

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

DebugLog(1, 'Watt: ' + str(wattbezug))
DebugLog(1, 'Einspeisung: ' + str(ekwh))
DebugLog(1, 'Bezug: ' + str(ikwh))
DebugLog(1, 'Leistung L1: ' + str(bezugw1))
DebugLog(1, 'Leistung L2: ' + str(bezugw2))
DebugLog(1, 'Leistung L3: ' + str(bezugw3))
DebugLog(1, 'Power Faktor L1: ' + str(evupf1))
DebugLog(1, 'Power Faktor L2: ' + str(evupf2))
DebugLog(1, 'Power Faktor L3: ' + str(evupf3))
DebugLog(1, 'Spannung L1: ' + str(evuv1))
DebugLog(1, 'Spannung L2: ' + str(evuv2))
DebugLog(1, 'Spannung L3: ' + str(evuv3))
DebugLog(1, 'Strom L1: ' + str(bezuga1))
DebugLog(1, 'Strom L2: ' + str(bezuga2))
DebugLog(1, 'Strom L3: ' + str(bezuga3))
DebugLog(1, 'Frequenz: ' + str(evuhz))

exit(0)