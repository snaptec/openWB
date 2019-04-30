#!/bin/bash
. /var/www/html/openWB/openwb.conf


answer=$(curl --connect-timeout 5 -s $wrjsonurl)
pvwatt=$(echo $answer | jq -r $wrjsonwatt | sed 's/\..*$//')
	if (( $pvwatt > 5 )); then
		pvwatt=$(echo "$pvwatt*-1" |bc)
	fi
echo $pvwatt
echo $pvwatt > /var/www/html/openWB/ramdisk/pvwatt

#WR-AC-Leistung muss in andere Datei für Berechnung Hausverbrauch
#zunächst hier den gleichen Wert wie für pvwatt nehmen bis Modul angepasst ist
echo $pvwatt > /var/www/html/openWB/ramdisk/wracwatt

pvkwh=$(echo $answer | jq -r $wrjsonkwh)
echo $pvkwh > /var/www/html/openWB/ramdisk/pvkwh
