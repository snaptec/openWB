#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
DMOD="MAIN"

# check if config file is already in env
if [[ -z "$debug" ]]; then
	echo "bezug_fronius_sm: Seems like openwb.conf is not loaded. Reading file."
	# try to load config
	. $OPENWBBASEDIR/loadconfig.sh
	# load helperFunctions
	. $OPENWBBASEDIR/helperFunctions.sh
fi

# for developement only
# debug=1

# Auslesen eines Fronius Symo WR mit Fronius Smartmeter über die integrierte JSON-API des WR.
# Rückgabewert ist die aktuelle Einspeiseleistung (negativ) oder Bezugsleistung (positiv).
# Einspeiseleistung: PV-Leistung > Verbrauch, es wird Strom eingespeist
# Bezugsleistug: PV-Leistung < Verbrauch, es wird Strom aus dem Netz bezogen

# Fordere die Werte vom SmartMeter an.
if [[ $froniusvar2 == "0" ]]; then
	# Setze die für JSON Abruf benötigte DeviceID
	json_id=".Body.Data"
	# Hole die JSON Daten
	response_sm=$(curl --connect-timeout 5 -s "$wrfroniusip/solar_api/v1/GetMeterRealtimeData.cgi?Scope=Device&DeviceId=$froniuserzeugung")

elif [[ $froniusvar2 == "1" ]]; then
	# Setze die für JSON Abruf benötigte DeviceID
	json_id=".Body.Data.\"$froniuserzeugung\""
	# Hole die JSON-Daten
	response_sm=$(curl --connect-timeout 5 -s "$wrfroniusip/solar_api/v1/GetMeterRealtimeData.cgi?Scope=System")
	# TODO: Evtl. ist es noch weiter zu vereinfachen -> selbe response_sm wie in Variante0 mit folgendem Aufruf:
	# response_sm=$(curl --connect-timeout 5 -s "$wrfroniusip/solar_api/v1/GetMeterRealtimeData.cgi?Scope=Device&DeviceID=$froniuserzeugung&DataCollection=MeterRealtimeData")
	# dann auch json_id wieder gleich:
	# json_id=".Body.Data"

elif [[ $froniusvar2 == "2" ]]; then
	# Setze die für JSON Abruf benötigte DeviceID
	json_id=".Body.Data.\"$froniuserzeugung\""
	# Hole die JSON-Daten
	response_sm=$(curl --connect-timeout 5 -s "$wrfroniusip/solar_api/v1/GetMeterRealtimeData.cgi?Scope=System")
	
	# TODO: meter_location für diese Variante korrekt ermitteln
	# Überprüfe den Einbauort des SmartMeters.
	meter_location=$froniusmeterlocation
	
	# Lese alle wichtigen Werte aus der JSON-Antwort und skaliere sie gleich.
	wattbezug=$(echo "scale=0; $(echo $response_sm | jq $json_id'.SMARTMETER_POWERACTIVE_MEAN_SUM_F64')/1" | bc)
	evuv1=$(echo "scale=2; $(echo $response_sm | jq $json_id'.SMARTMETER_VOLTAGE_01_F64')/1" | bc)
	evuv2=$(echo "scale=2; $(echo $response_sm | jq $json_id'.SMARTMETER_VOLTAGE_02_F64')/1" | bc)
	evuv3=$(echo "scale=2; $(echo $response_sm | jq $json_id'.SMARTMETER_VOLTAGE_03_F64')/1" | bc)
	bezugw1=$(echo "scale=2; $(echo $response_sm | jq $json_id'.SMARTMETER_POWERACTIVE_MEAN_01_F64')/1" | bc)
	bezugw2=$(echo "scale=2; $(echo $response_sm | jq $json_id'.SMARTMETER_POWERACTIVE_MEAN_02_F64')/1" | bc)
	bezugw3=$(echo "scale=2; $(echo $response_sm | jq $json_id'.SMARTMETER_POWERACTIVE_MEAN_03_F64')/1" | bc)
	# Berechne den Strom und lese ihn nicht direkt (der eigentlich zu lesende direkte Wert
	# "Current_AC_Phase_1" wäre der Absolutwert und man würde das Vorzeichen verlieren).
	bezuga1=$(echo "scale=2; $bezugw1 / $evuv1" | bc)
	bezuga2=$(echo "scale=2; $bezugw2 / $evuv2" | bc)
	bezuga3=$(echo "scale=2; $bezugw3 / $evuv3" | bc)
	evuhz=$(echo "scale=2; $(echo $response_sm | jq $json_id'.GRID_FREQUENCY_MEAN_F32')/1" | bc)
	evupf1=$(echo "scale=2; $(echo $response_sm | jq $json_id'.SMARTMETER_FACTOR_POWER_01_F64')/1" | bc)
	evupf2=$(echo "scale=2; $(echo $response_sm | jq $json_id'.SMARTMETER_FACTOR_POWER_02_F64')/1" | bc)
	evupf3=$(echo "scale=2; $(echo $response_sm | jq $json_id'.SMARTMETER_FACTOR_POWER_03_F64')/1" | bc)
	ikwh=$(echo $response_sm | jq $json_id'.SMARTMETER_ENERGYACTIVE_CONSUMED_SUM_F64')
	ekwh=$(echo $response_sm | jq $json_id'.SMARTMETER_ENERGYACTIVE_PRODUCED_SUM_F64')
fi

openwbDebugLog ${DMOD} 2 "EVU: response_sm: $response_sm"

# Auswertung für Variante0 und Variante1 gebündelt
if [[ $froniusvar2 != "2" ]]; then
	# Überprüfe den Einbauort des SmartMeters.
	meter_location=$(echo $response_sm | jq $json_id'.Meter_Location_Current')
	
	# Lese alle wichtigen Werte aus der JSON-Antwort und skaliere sie gleich.
	wattbezug=$(echo "scale=0; $(echo $response_sm | jq $json_id'.PowerReal_P_Sum')/1" | bc)
	evuv1=$(echo "scale=2; $(echo $response_sm | jq $json_id'.Voltage_AC_Phase_1')/1" | bc)
	evuv2=$(echo "scale=2; $(echo $response_sm | jq $json_id'.Voltage_AC_Phase_2')/1" | bc)
	evuv3=$(echo "scale=2; $(echo $response_sm | jq $json_id'.Voltage_AC_Phase_3')/1" | bc)
	bezugw1=$(echo "scale=2; $(echo $response_sm | jq $json_id'.PowerReal_P_Phase_1')/1" | bc)
	bezugw2=$(echo "scale=2; $(echo $response_sm | jq $json_id'.PowerReal_P_Phase_2')/1" | bc)
	bezugw3=$(echo "scale=2; $(echo $response_sm | jq $json_id'.PowerReal_P_Phase_3')/1" | bc)
	# Berechne den Strom und lese ihn nicht direkt (der eigentlich zu lesende direkte Wert
	# "Current_AC_Phase_1" wäre der Absolutwert und man würde das Vorzeichen verlieren).
	bezuga1=$(echo "scale=2; $bezugw1 / $evuv1" | bc)
	bezuga2=$(echo "scale=2; $bezugw2 / $evuv2" | bc)
	bezuga3=$(echo "scale=2; $bezugw3 / $evuv3" | bc)
	evuhz=$(echo "scale=2; $(echo $response_sm | jq $json_id'.Frequency_Phase_Average')/1" | bc)
	evupf1=$(echo "scale=2; $(echo $response_sm | jq $json_id'.PowerFactor_Phase_1')/1" | bc)
	evupf2=$(echo "scale=2; $(echo $response_sm | jq $json_id'.PowerFactor_Phase_2')/1" | bc)
	evupf3=$(echo "scale=2; $(echo $response_sm | jq $json_id'.PowerFactor_Phase_3')/1" | bc)
	ikwh=$(echo $response_sm | jq $json_id'.EnergyReal_WAC_Sum_Consumed')
	ekwh=$(echo $response_sm | jq $json_id'.EnergyReal_WAC_Sum_Produced')

fi

openwbDebugLog ${DMOD} 1 "EVU: SmartMeter location: $meter_location"

if [[ $meter_location == "1" ]]; then
	# wenn SmartMeter im Verbrauchszweig sitzt sind folgende Annahmen getroffen:
	# PV Leistung wird gleichmäßig auf alle Phasen verteilt
	# Spannungen und Leistungsfaktoren sind am Verbrauchszweig == Einspeisepunkt

	# Lese die aktuelle PV-Leistung des Wechselrichters ein.
	response_fi=$(curl --connect-timeout 3 -s "$wrfroniusip/solar_api/v1/GetPowerFlowRealtimeData.fcgi?Scope=System")
	openwbDebugLog ${DMOD} 1 "EVU: response_fi: $response_fi"
	# Basis ist die Leistungsangabe aus dem WR!
	wattbezug=$(echo "scale=0; $(echo $response_fi | jq '.Body.Data.Site.P_Grid')/1" | bc)
	pvwatt=$(echo $response_fi | jq '.Body.Data.Site.P_PV' | sed 's/\..*$//')
	# Wenn WR aus bzw. im Standby (keine Antwort), ersetze leeren Wert durch eine 0.
	re='^-?[0-9]+$'
	if ! [[ $pvwatt =~ $re ]] ; then
		pvwatt="0"
	fi
	# Hier gehen wir mal davon aus, dass der Wechselrichter seine PV-Leistung gleichmäßig auf alle Phasen aufteilt.
	bezugw1=$(echo "scale=2; (-1 * $(echo $bezugw1) - $pvwatt/3)/1" | bc)
	bezugw2=$(echo "scale=2; (-1 * $(echo $bezugw2) - $pvwatt/3)/1" | bc)
	bezugw3=$(echo "scale=2; (-1 * $(echo $bezugw3) - $pvwatt/3)/1" | bc)
	# Wegen der geänderten Leistungen sind die Ströme erneut zu berechnen
	bezuga1=$(echo "scale=2; $bezugw1 / $evuv1" | bc)
	bezuga2=$(echo "scale=2; $bezugw2 / $evuv2" | bc)
	bezuga3=$(echo "scale=2; $bezugw3 / $evuv3" | bc)
	# Beim Energiebezug ist nicht klar, welcher Anteil aus dem Netz bezogen wurde, und was aus dem Wechselrichter kam.
	#ikwh=$(echo $response_sm | jq '.Body.Data.EnergyReal_WAC_Sum_Consumed')
	ikwh=0
	# Beim Energieexport ist nicht klar, wie hoch der Eigenverbrauch während der Produktion war.
	#ekwh=$(echo $response_fi | jq '.Body.Data.Site.E_Total')
	ekwh=0
	echo 1 > /var/www/html/openWB/ramdisk/fronius_sm_bezug_meterlocation

fi

openwbDebugLog ${DMOD} 1 "EVU: V: ${evuv1}/${evuv2}/${evuv3} A: ${bezuga1}/${bezuga2}/${bezuga3} W: ${bezugw1}/${bezugw2}/${bezugw3}/T${wattbezug}"

# Gib den wichtigsten Wert direkt zurück (auch sinnvoll beim Debuggen).
echo $wattbezug

# Schreibe alle Werte in die Ramdisk.
echo $wattbezug > /var/www/html/openWB/ramdisk/wattbezug
echo $evuv1 > /var/www/html/openWB/ramdisk/evuv1
echo $evuv2 > /var/www/html/openWB/ramdisk/evuv2
echo $evuv3 > /var/www/html/openWB/ramdisk/evuv3
echo $bezugw1 > /var/www/html/openWB/ramdisk/bezugw1
echo $bezugw2 > /var/www/html/openWB/ramdisk/bezugw2
echo $bezugw3 > /var/www/html/openWB/ramdisk/bezugw3
echo $bezuga1 > /var/www/html/openWB/ramdisk/bezuga1
echo $bezuga2 > /var/www/html/openWB/ramdisk/bezuga2
echo $bezuga3 > /var/www/html/openWB/ramdisk/bezuga3
echo $evuhz > /var/www/html/openWB/ramdisk/evuhz
echo $evupf1 > /var/www/html/openWB/ramdisk/evupf1
echo $evupf2 > /var/www/html/openWB/ramdisk/evupf2
echo $evupf3 > /var/www/html/openWB/ramdisk/evupf3
echo $ikwh > /var/www/html/openWB/ramdisk/bezugkwh
echo $ekwh > /var/www/html/openWB/ramdisk/einspeisungkwh
