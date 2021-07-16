#!/bin/bash

# Auslesen eines Solarworl eManagers über die integrierte JSON-API
emanagerantwort=$(curl --connect-timeout 5 -s "$solarworld_emanagerip/rest/solarworld/lpvm/powerAndBatteryData")

em_in_watt=$(echo $emanagerantwort | jq '.PowerIn')
em_out_watt=$(echo $emanagerantwort | jq '.PowerOut')

# Bezug ist entweder -Out oder In; bei Einspeisung ist 'em_in_watt' immer 0
# use printf zum runden, LC_ALL=C wegen Dezimalpunkt
bezug_watt=$(LC_ALL=C printf "%.0f\n" $(echo "$em_in_watt - $em_out_watt" | bc))

#wenn eManager aus bzw. keine Antwort ersetze leeren Wert durch eine 0
ra='^-?[0-9]+$'

if ! [[ $bezug_watt =~ $ra ]] ; then
	bezug_watt="0"
fi
echo $bezug_watt
echo $bezug_watt > /var/www/html/openWB/ramdisk/wattbezug
