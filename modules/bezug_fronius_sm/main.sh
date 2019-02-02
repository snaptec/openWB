#!/bin/bash

#Auslesen eines Fronius Symo WR mit Fronius Smartmeter über die integrierte JSON-API des WR.
#Rückgabewert ist die aktuelle Einspeiseleistung (negativ) oder Bezugsleistung (positiv)
# Einspeiseleistung: PV-Leistung > Verbrauch, es wird Strom eingespeist
# Bezugsleistug: PV-Leistung < Verbrauch, es wird Strom aus dem Netz bezogen
. /var/www/html/openWB/openwb.conf

#wattbezugtmp=$(curl --connect-timeout 5 -s $wrfroniusip/solar_api/v1/GetPowerFlowRealtimeData.fcgi)  // temporaer umgestellt
#wattbezug=$(echo $wattbezugtmp | jq '.Body.Data.Site.P_Grid' |sed 's/\..*$//') // temporaer umgestellt

#Aenderung von Powerflow auf MeterRealtime da hier noch die A je Phase fuer das Lastmanagement zur Verfuegung stehen
wattbezugtmp=$(curl -s "$wrfroniusip/solar_api/v1/GetMeterRealtimeData.cgi?Scope=Device&DeviceID=0")
wattbezug=$(echo $wattbezugtmp | jq '.Body.Data.PowerReal_P_Sum' | sed 's/\..*$//')
bezuga1=$(echo $wattbezugtmp | jq '.Body.Data.PowerReal_P_Phase_1')
bezuga2=$(echo $wattbezugtmp | jq '.Body.Data.PowerReal_P_Phase_2')
bezuga3=$(echo $wattbezugtmp | jq '.Body.Data.PowerReal_P_Phase_3')
volt1=$(echo $wattbezugtmp | jq '.Body.Data.Voltage_AC_Phase_1')
volt2=$(echo $wattbezugtmp | jq '.Body.Data.Voltage_AC_Phase_2')
volt3=$(echo $wattbezugtmp | jq '.Body.Data.Voltage_AC_Phase_3')
bezuga1=$(echo "scale=2; $bezuga1 / $volt1" | bc)
bezuga2=$(echo "scale=2; $bezuga2 / $volt2" | bc)
bezuga3=$(echo "scale=2; $bezuga3 / $volt3" | bc)
echo $bezuga1 > /var/www/html/openWB/ramdisk/bezuga1
echo $bezuga2 > /var/www/html/openWB/ramdisk/bezuga2
echo $bezuga3 > /var/www/html/openWB/ramdisk/bezuga3





#wenn WR aus bzw. im standby (keine Antwort) ersetze leeren Wert durch eine 0
re='^[0-9]+$'
ra='^-[0-9]+$'
if ! [[ $wattbezug =~ $re ]] ; then
	  if ! [[ $wattbezug =~ $ra ]] ; then
		  wattbezug="0"
	  fi
fi

echo $wattbezug
#zur weiteren verwendung im webinterface


echo $wattbezug > /var/www/html/openWB/ramdisk/wattbezug


# Summe der vom Netz bezogene Energie total in Wh
# nur für Smartmeter  im Einspeisepunkt!
# bei Smartmeter im Verbrauchszweig  entspricht das dem Gesamtverbrauch
kwhtmp=$(curl --connect-timeout 5 -s $wrfroniusip/solar_api/v1/GetMeterRealtimeData.cgi?Scope=System)
# jq-Funktion funktioniert hier leider nicht,  wegen "0" als Bezeichnung

ekwh=$(echo ${kwhtmp##*EnergyReal_WAC_Minus_Absolute} | tr -d ' ' |  tr -d '\"' | tr -d ':' | tr -d '}' | tr -d '\n')

# bei Smartmeter im Verbrauchsweig immer 0
ikwh=$(echo ${kwhtmp##*EnergyReal_WAC_Plus_Absolute} | sed 's/,.*//' | tr -d ' ' | tr -d ':' | tr -d '\"')
echo $ikwh > /var/www/html/openWB/ramdisk/bezugkwh
echo $ekwh > /var/www/html/openWB/ramdisk/einspeisungkwh
