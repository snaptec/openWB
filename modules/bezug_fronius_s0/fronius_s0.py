#!/usr/bin/env python3
# coding: utf8
from datetime import datetime, timezone
import os
import requests
import sys

# Auslesen eines Fronius Symo WR mit Fronius Smartmeter über die integrierte JSON-API des WR.
# Rückgabewert ist die aktuelle Einspeiseleistung (negativ) oder Bezugsleistung (positiv)
# Einspeiseleistung: PV-Leistung > Verbrauch, es wird Strom eingespeist
# Bezugsleistug: PV-Leistung < Verbrauch, es wird Strom aus dem Netz bezogen
primo = str(sys.argv[1])
ip_address = str(sys.argv[2])

Debug = int(os.environ.get('debug'))
myPid = str(os.getpid())

def DebugLog(level, message):
    if Debug >= level:
        local_time = datetime.now(timezone.utc).astimezone()
        print(local_time.strftime(format="%Y-%m-%d %H:%M:%S") + ": PID: " + myPid + ": " + message)

DebugLog(2, 'Fronius S0 Primo: ' + primo)
DebugLog(2, 'Fronius SM IP: ' + ip_address)

response_fi = requests.get('http://'+ip_address+'/solar_api/v1/GetPowerFlowRealtimeData.fcgi', timeout = 5)
response = response_fi.json()
DebugLog(1, 'response_fi: ' + str(response_fi))
DebugLog(2, 'response_fi_data: ' + str(response))
if primo == str(1):
    # Ohne PV Produktion liefert der WR 'null', ersetze durch Zahl 0
    wattbezug=int(response["Body"]["Data"]["Site"]["P_Grid"] or 0)
else:
    # Ohne PV Produktion liefert der WR 'null', ersetze durch Zahl 0
    wattbezug=int(response["Body"]["Data"]["PowerReal_P_Sum"] or 0)

#pvwatttmp=$(curl --connect-timeout 5 -s $wrfroniusip/solar_api/v1/GetInverterRealtimeData.cgi?Scope=System)
#pvwatt=$(echo $pvwatttmp | jq '.Body.Data.PAC.Values' | sed 's/.*://' | tr -d '\n' | sed 's/^.\{2\}//' | sed 's/.$//' )
with open( "ramdisk/pvwatt" , 'r') as f:
    pvwatt =int(f.read())

# zur weiteren verwendung im webinterface
with open('/var/www/html/openWB/ramdisk/wattbezug', 'w') as f:
    f.write(str(wattbezug))

# Summe der vom Netz bezogene Energie total in Wh
# nur für Smartmeter  im Einspeisepunkt!
# bei Smartmeter im Verbrauchszweig  entspricht das dem Gesamtverbrauch
params = (('Scope', 'System'),)

response_s0 = requests.get('http://'+ip_address+'/solar_api/v1/GetMeterRealtimeData.cgi', params=params, timeout = 5)
response = response_s0.json()
DebugLog(1, 'response_s0: ' + str(response_fi))
DebugLog(2, 'response_s0_data: ' + str(response))
# jq-Funktion funktioniert hier leider nicht,  wegen "0" als Bezeichnung
for location in response["Body"]["Data"]:
    if "EnergyReal_WAC_Minus_Absolute" in response["Body"]["Data"][location]:
        ikwh = response["Body"]["Data"][location]["EnergyReal_WAC_Minus_Absolute"]
    else:
        with open('/var/www/html/openWB/ramdisk/bezugkwh', 'r') as f:
            ikwh = float(f.read())
        if wattbezug > 0:
            # OpenWB Regelintervall 10s, Intervallfrequenz 360/h
            ikwh += float(wattbezug) / 360

#ikwh=$(echo ${kwhtmp##*EnergyReal_WAC_Minus_Absolute} | tr -d ' ' |  tr -d '\"' | tr -d ':' | tr -d '}' | tr -d '\n')
#echo $ikwh #Test-Ausgabe
with open('/var/www/html/openWB/ramdisk/bezugkwh', 'w') as f:
    f.write(str(ikwh))

# Eingespeiste Energie total in Wh (für Smartmeter im Einspeisepunkt)
# bei Smartmeter im Verbrauchsweig immer 0
#ekwh=$(echo ${kwhtmp##*EnergyReal_WAC_Plus_Absolute} | sed 's/,.*//' | tr -d ' ' | tr -d ':' | tr -d '\"')
for location in response["Body"]["Data"]:
    if "EnergyReal_WAC_Plus_Absolute" in response["Body"]["Data"][location]:
        ekwh = response["Body"]["Data"][location]["EnergyReal_WAC_Plus_Absolute"]
    else:
        with open('/var/www/html/openWB/ramdisk/einspeisungkwh', 'r') as f:
            ekwh = float(f.read())
        if wattbezug < 0:
            # OpenWB Regelintervall 10s, Intervallfrequenz 360/h
            ekwh += float(abs(wattbezug)) / 360

with open('/var/www/html/openWB/ramdisk/einspeisungkwh', 'w') as f:
    f.write(str(ekwh))