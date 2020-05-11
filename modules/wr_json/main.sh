#!/bin/bash


answer=$(curl --connect-timeout 5 -s $wrjsonurl)
pvwatt=$(echo $answer | jq -r $wrjsonwatt | sed 's/\..*$//')
	if (( $pvwatt > 5 )); then
		pvwatt=$(echo "$pvwatt*-1" |bc)
	fi	
echo $pvwatt
echo $pvwatt > /var/www/html/openWB/ramdisk/pvwatt
pvkwh=$(echo $answer | jq -r $wrjsonkwh)
echo $pvkwh > /var/www/html/openWB/ramdisk/pvkwh
