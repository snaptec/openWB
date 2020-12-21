#!/bin/bash

re='^[-+]?[0-9]+\.?[0-9]*$'
answer=$(curl --connect-timeout 5 -s $wr2jsonurl)
pvwatt=$(echo $answer | jq -r $wr2jsonwatt | sed 's/\..*$//')
	if (( $pvwatt > 5 )); then
		pvwatt=$(echo "$pvwatt*-1" |bc)
	fi

if ! [[ $pvwatt =~ $re ]] ; then
	   pvwatt=$(</var/www/html/openWB/ramdisk/pv2watt)
fi
echo $pvwatt > /var/www/html/openWB/ramdisk/pv2watt
pv2kwh=$(echo $answer | jq -r $wr2jsonkwh)
if ! [[ $pv2kwh =~ $re ]] ; then
	   pv2kwh=$(</var/www/html/openWB/ramdisk/pv2kwh)
fi

echo $pv2kwh > /var/www/html/openWB/ramdisk/pv2kwh

pv2watt=$(</var/www/html/openWB/ramdisk/pv2watt)

echo $pv2watt
