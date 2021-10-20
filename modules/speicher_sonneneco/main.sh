#!/bin/bash

# Auslesen einer Sonnbenbatterie Eco 4.5 über die integrierte JSON-API des Batteriesystems
ra='^-?[0-9]+$'
if (( sonnenecoalternativ == 2 )); then
	speichersoc=$(curl --connect-timeout 5 -s "$sonnenecoip:7979/rest/devices/battery/M05")
	speichersoc=$(echo $speichersoc | sed 's/\..*$//')
	speicherentladung=$(curl --connect-timeout 5 -s "$sonnenecoip:7979/rest/devices/battery/M01")
	speicherladung=$(curl --connect-timeout 5 -s "$sonnenecoip:7979/rest/devices/battery/M02")
	speicherladung=$(echo $speicherladung | sed 's/\..*$//')
	speicherentladung=$(echo $speicherentladung | sed 's/\..*$//')
	speicherwatt=$(echo "$speicherladung - $speicherentladung" | bc)
	# wenn Batterie aus bzw. keine Antwort ersetze leeren Wert durch eine 0
	if ! [[ $speicherwatt =~ $ra ]] ; then
		speicherwatt="0"
	fi
	echo $speicherwatt > /var/www/html/openWB/ramdisk/speicherleistung
	if ! [[ $speichersoc =~ $ra ]] ; then
		speichersoc="0"
	fi
	echo $speichersoc > /var/www/html/openWB/ramdisk/speichersoc
	pvwatt=$(curl --connect-timeout 5 -s "$sonnenecoip:7979/rest/devices/battery/M03")
	pvwatt=$(echo $pvwatt | sed 's/\..*$//')
	pvwatt=$(( pvwatt * -1))
	echo $pvwatt > /var/www/html/openWB/ramdisk/pvwatt
else
	if (( sonnenecoalternativ == 0 )); then
		speicherantwort=$(curl --connect-timeout 5 -s "$sonnenecoip:7979/rest/devices/battery")
		speichersoc=$(echo $speicherantwort | jq '.M05' | sed 's/\..*$//')
		speicherentladung=$(echo $speicherantwort | jq '.M34' | sed 's/\..*$//')
		speicherladung=$(echo $speicherantwort | jq '.M35' |sed 's/\..*$//')
		speicherwatt=$(echo "$speicherladung - $speicherentladung" | bc)
		# wenn Batterie aus bzw. keine Antwort ersetze leeren Wert durch eine 0
		if ! [[ $speicherwatt =~ $ra ]] ; then
			speicherwatt="0"
		fi
		echo $speicherwatt > /var/www/html/openWB/ramdisk/speicherleistung
		if ! [[ $speichersoc =~ $ra ]] ; then
			speichersoc="0"
		fi
		echo $speichersoc > /var/www/html/openWB/ramdisk/speichersoc
	else
		speicherantwort=$(curl --connect-timeout 5 -s "$sonnenecoip/api/v1/status")
		speicherwatt=$(echo $speicherantwort | jq .Pac_total_W)
		speichersoc=$(echo $speicherantwort | jq .USOC)
		speicherpvwatt=$(echo $speicherantwort | jq .Production_W)
		speicherpvwatt=$((speicherpvwatt * -1))
		echo $speicherpvwatt > /var/www/html/openWB/ramdisk/pvwatt
		if ! [[ $speicherwatt =~ $ra ]] ; then
			speicherwatt="0"
		else
			speicherwatt=$((speicherwatt * -1))
		fi
		echo $speicherwatt > /var/www/html/openWB/ramdisk/speicherleistung
		if ! [[ $speichersoc =~ $ra ]] ; then
			speichersoc="0"
		fi
		echo $speichersoc > /var/www/html/openWB/ramdisk/speichersoc
	fi
fi
