#!/bin/bash

# Auslesen eines Solarworld eManagers über die integrierte JSON-API
emanagerantwort=$(curl --connect-timeout 5 -s "$solarworld_emanagerip/rest/solarworld/lpvm/powerAndBatteryData")

wr_watt=$(LC_ALL=C printf "%.0f\n" $(echo $emanagerantwort | jq '.PowerTotalPV'))

# wenn eManager aus bzw. keine Antwort ersetze leeren Wert durch eine 0
ra='^-?[0-9]+$'

if ! [[ $wr_watt =~ $ra ]] ; then
	wr_watt="0"
fi

# PV ezeugte Leistung muss negativ sein
pvwatt=$(echo "0 - $wr_watt" | bc)
echo $pvwatt
echo $pvwatt  > /var/www/html/openWB/ramdisk/pvwatt
