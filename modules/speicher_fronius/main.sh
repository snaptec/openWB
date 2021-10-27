#!/bin/bash

#Auslesen eines Fronius Symo WR Hybrid mit Fronius Smartmeter und Batterie über die integrierte JSON-API des WR.

speicherwatttmp=$(curl --connect-timeout 5 -s "$wrfroniusip/solar_api/v1/GetPowerFlowRealtimeData.fcgi?Scope=System")
speicherwatt=$(echo $speicherwatttmp | jq '.Body.Data.Site.P_Akku' | sed 's/\..*$//')
speicherwatt=$(echo "$speicherwatt * -1" | bc)
#wenn WR aus bzw. im standby (keine Antwort) ersetze leeren Wert durch eine 0
ra='^-?[0-9]+$'
if ! [[ $speicherwatt =~ $ra ]] ; then
	speicherwatt="0"
fi

echo $speicherwatt > /var/www/html/openWB/ramdisk/speicherleistung


if [[ $wrfroniusisgen24 == 1 ]]; then
	speichersoctmp=$(curl --connect-timeout 5 -s "$wrfroniusip/solar_api/v1/GetStorageRealtimeData.cgi")
	speichersoc=$(echo $speichersoctmp | jq '.Body.Data."1".Controller.StateOfCharge_Relative' | sed 's/\..*$//')
else
	speichersoc=$(echo $speicherwatttmp | jq '.Body.Data.Inverters."1".SOC' | sed 's/\..*$//')
fi
if ! [[ $speichersoc =~ $ra ]] ; then
	speichersoc="0"
fi

echo $speichersoc > /var/www/html/openWB/ramdisk/speichersoc
