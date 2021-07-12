#!/bin/bash

answer=$(curl -d {\"801\":{\"170\":null}} --connect-timeout 5 -s $bezug_solarlog_ip/getjp)

pvwatt=$(echo $answer | jq '."801"."170"."101"' )
hausverbrauch=$(echo $answer | jq '."801"."170"."110"' )
bezugwatt=$(echo "$hausverbrauch - $pvwatt" |bc) 
pvkwh=$(echo $answer | jq '."801"."170"."109"' )

if (( bezug_solarlog_speicherv == 1 )); then
	speicherleistung=$(<ramdisk/speicherleistung)
	bezugwatt=$(( bezugwatt + speicherleistung ))
fi
if (( $pvwatt > 5 )); then
	pvwatt=$(echo "$pvwatt*-1" |bc)
fi
echo $bezugwatt
echo $bezugwatt > /var/www/html/openWB/ramdisk/wattbezug
echo $pvwatt > /var/www/html/openWB/ramdisk/pvwatt
echo $pvkwh > /var/www/html/openWB/ramdisk/pvkwh
pvkwhk=$(echo "$pvkwh*1000" |bc)
echo $pvkwhk > /var/www/html/openWB/ramdisk/pvkwhk
