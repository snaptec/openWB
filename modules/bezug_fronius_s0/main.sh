#!/bin/bash

# Auslesen eines Fronius Symo WR mit Fronius Smartmeter über die integrierte JSON-API des WR.
# Rückgabewert ist die aktuelle Einspeiseleistung (negativ) oder Bezugsleistung (positiv)
# Einspeiseleistung: PV-Leistung > Verbrauch, es wird Strom eingespeist
# Bezugsleistug: PV-Leistung < Verbrauch, es wird Strom aus dem Netz bezogen

wattbezugtmp=$(curl --connect-timeout 5 -s $wrfroniusip/solar_api/v1/GetPowerFlowRealtimeData.fcgi)
if (( froniusprimo == 1 )); then
	wattbezug=$(echo $wattbezugtmp | jq -r '.Body.Data.Site.P_Grid' |sed 's/\..*$//')
else
	wattbezug=$(echo $wattbezugtmp | jq -r '.Body.Data.PowerReal_P_Sum' |sed 's/\..*$//')
fi
#pvwatttmp=$(curl --connect-timeout 5 -s $wrfroniusip/solar_api/v1/GetInverterRealtimeData.cgi?Scope=System)
#pvwatt=$(echo $pvwatttmp | jq '.Body.Data.PAC.Values' | sed 's/.*://' | tr -d '\n' | sed 's/^.\{2\}//' | sed 's/.$//' )
pvwatt=$(<ramdisk/pvwatt)
wattb=$(( pvwatt + wattbezug ))

#wenn WR aus bzw. im standby (keine Antwort) ersetze leeren Wert durch eine 0
re='^[0-9]+$'
ra='^-[0-9]+$'
if ! [[ $wattbezug =~ $re ]] ; then
	if ! [[ $wattbezug =~ $ra ]] ; then
		wattbezug="0"
	fi
fi

echo $wattbezug
# zur weiteren verwendung im webinterface
echo $wattbezug > /var/www/html/openWB/ramdisk/wattbezug
# Summe der vom Netz bezogene Energie total in Wh
# nur für Smartmeter  im Einspeisepunkt!
# bei Smartmeter im Verbrauchszweig  entspricht das dem Gesamtverbrauch
kwhtmp=$(curl --connect-timeout 5 -s $wrfroniusip/solar_api/v1/GetMeterRealtimeData.cgi?Scope=System)
# jq-Funktion funktioniert hier leider nicht,  wegen "0" als Bezeichnung
ikwh=$(echo ${kwhtmp##*EnergyReal_WAC_Minus_Absolute} | tr -d ' ' |  tr -d '\"' | tr -d ':' | tr -d '}' | tr -d '\n')
#echo $ikwh #Test-Ausgabe
echo $ikwh > /var/www/html/openWB/ramdisk/bezugkwh
# Eingespeiste Energie total in Wh (für Smartmeter im Einspeisepunkt)
# bei Smartmeter im Verbrauchsweig immer 0
ekwh=$(echo ${kwhtmp##*EnergyReal_WAC_Plus_Absolute} | sed 's/,.*//' | tr -d ' ' | tr -d ':' | tr -d '\"')
#echo $ekwh #Test-Ausgabe
echo $ekwh > /var/www/html/openWB/ramdisk/einspeisungkwh
