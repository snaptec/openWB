#!/bin/bash


answer=$(curl -k --connect-timeout 5 -s "https://$speicherpwip/api/meters/aggregates")
pvwatt=$(echo $answer | jq -r '.solar.instant_power' | sed 's/\..*$//')
if (( $pvwatt > 5 )); then
	pvwatt=$(echo "$pvwatt*-1" |bc)
fi
echo $pvwatt
echo $pvwatt > /var/www/html/openWB/ramdisk/pvwatt
pvkwh=$(echo $answer | jq -r '.solar.energy_exported')
echo $pvkwh > /var/www/html/openWB/ramdisk/pvkwh
