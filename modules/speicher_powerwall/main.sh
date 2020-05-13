#!/bin/bash


speicherwatttmp=$(curl -k --connect-timeout 5 -s "https://$speicherpwip/api/meters/aggregates")


speicherwatt=$(echo $speicherwatttmp | jq .battery.instant_power | sed 's/\..*$//')
speicherwatt=$(echo "$speicherwatt * -1" | bc)
ra='^[-+]?[0-9]+\.?[0-9]*$'
if ! [[ $speicherwatt =~ $ra ]] ; then
		  speicherwatt="0"
fi

echo $speicherwatt > /var/www/html/openWB/ramdisk/speicherleistung

speichersoc=$(curl -k --connect-timeout 5 -s "https://$speicherpwip/api/system_status/soe")
soc=$(echo $speichersoc | jq .percentage)
soc=$(echo "($soc+0.5)/1" | bc)
if ! [[ $soc =~ $ra ]] ; then
	soc="0"
fi


echo $soc > /var/www/html/openWB/ramdisk/speichersoc
