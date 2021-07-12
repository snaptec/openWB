#!/bin/bash

answer=$(curl -d {\"801\":{\"170\":null}} --connect-timeout 5 -s $bezug_solarlog_ip/getjp)
pvwatt=$(echo $answer | jq '."801"."170"."101"' )
pvkwh=$(echo $answer | jq '."801"."170"."109"' )

if (( $pvwatt > 5 )); then
	pvwatt=$(echo "$pvwatt*-1" |bc)
fi
echo $pvwatt
echo $pvwatt > /var/www/html/openWB/ramdisk/pvwatt
echo $pvkwh > /var/www/html/openWB/ramdisk/pvkwh
