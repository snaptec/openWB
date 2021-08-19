#!/usr/bin/env python3
# coding: utf8

import re
import requests
import sys
import traceback

# Auslesen eines Fronius Symo WR mit Fronius Smartmeter über die integrierte JSON-API des WR.
# Rückgabewert ist die aktuelle Einspeiseleistung (negativ) oder Bezugsleistung (positiv)
# Einspeiseleistung: PV-Leistung > Verbrauch, es wird Strom eingespeist
# Bezugsleistug: PV-Leistung < Verbrauch, es wird Strom aus dem Netz bezogen
primo = str(sys.argv[1])
ip_address = str(sys.argv[2])

response = requests.get('http://'+ip_address+'/solar_api/v1/GetPowerFlowRealtimeData.fcgi', timeout = 5).json()
try:
    if primo == str(1):
        wattbezug=int(response["Body"]["Data"]["Site"]["P_Grid"])
    else:
        wattbezug=int(response["Body"]["Data"]["PowerReal_P_Sum"])
except:
    traceback.print_exc()

#pvwatttmp=$(curl --connect-timeout 5 -s $wrfroniusip/solar_api/v1/GetInverterRealtimeData.cgi?Scope=System)
#pvwatt=$(echo $pvwatttmp | jq '.Body.Data.PAC.Values' | sed 's/.*://' | tr -d '\n' | sed 's/^.\{2\}//' | sed 's/.$//' )
f = open( "ramdisk/pvwatt" , 'r')
pvwatt =int(f.read())
f.close()
wattb=pvwatt + wattbezug

#wenn WR aus bzw. im standby (keine Antwort) ersetze leeren Wert durch eine 0
regex='^[0-9]+$'
ra='^-[0-9]+$'
if re.search(regex, str(wattbezug)) == None:
    if re.search(ra, str(wattbezug)) == None:
        wattbezug=0

# zur weiteren verwendung im webinterface
f = open('/var/www/html/openWB/ramdisk/wattbezug', 'w')
f.write(str(wattbezug))
f.close()
# Summe der vom Netz bezogene Energie total in Wh
# nur für Smartmeter  im Einspeisepunkt!
# bei Smartmeter im Verbrauchszweig  entspricht das dem Gesamtverbrauch
params = (('Scope', 'System'),)

kwhtmp = requests.get('http://'+ip_address+'/solar_api/v1/GetMeterRealtimeData.cgi', params=params, timeout = 5).json()
# jq-Funktion funktioniert hier leider nicht,  wegen "0" als Bezeichnung
try:
    for location in kwhtmp["Body"]["Data"]:
        ikwh = str(kwhtmp["Body"]["Data"][location]["EnergyReal_WAC_Minus_Absolute"])
except:
    traceback.print_exc()
ikwh = ikwh.replace(" ", "")
ikwh = ikwh.replace('\"', "")
ikwh = ikwh.replace(':', "")
ikwh = ikwh.replace('}', "")
ikwh = ikwh.replace('\n', "")

#ikwh=$(echo ${kwhtmp##*EnergyReal_WAC_Minus_Absolute} | tr -d ' ' |  tr -d '\"' | tr -d ':' | tr -d '}' | tr -d '\n')
#echo $ikwh #Test-Ausgabe
f = open('/var/www/html/openWB/ramdisk/bezugkwh', 'w')
f.write(str(ikwh))
f.close()
# Eingespeiste Energie total in Wh (für Smartmeter im Einspeisepunkt)
# bei Smartmeter im Verbrauchsweig immer 0
#ekwh=$(echo ${kwhtmp##*EnergyReal_WAC_Plus_Absolute} | sed 's/,.*//' | tr -d ' ' | tr -d ':' | tr -d '\"')
try:
    for location in kwhtmp["Body"]["Data"]:
        ekwh = str(kwhtmp["Body"]["Data"][location]["EnergyReal_WAC_Plus_Absolute"])
except:
    traceback.print_exc()
ekwh = ekwh.split(",")[0]
ekwh = ekwh.replace(" ", "")
ekwh = ekwh.replace('\"', "")
ekwh = ekwh.replace(':', "")
#echo $ekwh #Test-Ausgabe
f = open('/var/www/html/openWB/ramdisk/einspeisungkwh', 'w')
f.write(str(ekwh))
f.close()