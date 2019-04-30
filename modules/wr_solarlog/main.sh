#!/bin/bash


. /var/www/html/openWB/openwb.conf


answer=$(curl -d {\"801\":{\"170\":null}} --connect-timeout 5 -s $bezug_solarlog_ip/getjp)

pvwatt=$(echo $answer | jq '."801"."170"."101"' )
pvkwh=$(echo $answer | jq '."801"."170"."109"' )


if (( $pvwatt > 5 )); then
	pvwatt=$(echo "$pvwatt*-1" |bc)
fi
echo $pvwatt
echo $pvwatt > /var/www/html/openWB/ramdisk/pvwatt

#WR-AC-Leistung muss in andere Datei für Berechnung Hausverbrauch
#zunächst hier den gleichen Wert wie für pvwatt nehmen bis Modul angepasst ist
echo $pvwatt > /var/www/html/openWB/ramdisk/wracwatt

echo $pvkwh > /var/www/html/openWB/ramdisk/pvkwh
