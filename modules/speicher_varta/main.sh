#!/bin/bash

# Auslesen eines Varta Speicher über die integrierte XML-API der Batteroe.

if [[ "$usevartamodbus" != "1" ]]; then
	speicherwatt=$(curl --connect-timeout 5 -s "$vartaspeicherip/cgi/ems_data.xml" | grep 'P' | sed 's/.*value=//' |tr -d "'/>")
	# wenn WR aus bzw. im standby (keine Antwort) ersetze leeren Wert durch eine 0
	ra='^-?[0-9]+$'
	if [[ $speicherwatt =~ $ra ]] ; then
		echo $speicherwatt > /var/www/html/openWB/ramdisk/speicherleistung
	fi
	speichersoc=$(curl --connect-timeout 5 -s "$vartaspeicherip/cgi/ems_data.xml" | grep 'SOC' | sed 's/.*value=//' |tr -d "'/>")
	# if [[ $speichersoc -ge "101" ]]; then
	speichersoc=$(echo "$speichersoc / 10" |bc)
	# fi
	if [[ $speichersoc =~ $ra ]] ; then
		echo $speichersoc > /var/www/html/openWB/ramdisk/speichersoc
	fi
else 
	python /var/www/html/openWB/modules/speicher_varta/varta.py $vartaspeicherip $vartaspeicher2ip
fi
