#!/bin/bash

. /var/www/html/openWB/openwb.conf

speicherwatttmp=$(curl --connect-timeout 5 -s "$speicherpwip/api/meters/aggregates")


speicherwatt=$(echo $speicherwatttmp | jq .battery.instant_power)
speicherwatt=$(echo "$speicherwatt * -1" | bc)
ra='^-?[0-9]+$'
if ! [[ $speicherwatt =~ $ra ]] ; then
		  speicherwatt="0"
fi

echo $speicherwatt > /var/www/html/openWB/ramdisk/speicherleistung

speichersoc=$(curl --connect-timeout 5 -s "$speicherpwip/api/system_status/soe")
soc=$(echo $speichersoc | jq .percentage)
if ! [[ $soc =~ $ra ]] ; then
	soc="0"
fi


echo $soc > /var/www/html/openWB/ramdisk/speichersoc

