#!/bin/bash

#Auslesen eines Varta Speicher über die integrierte XML-API der Batteroe.
. /var/www/html/openWB/openwb.conf

speicherwatttmp=$(curl --connect-timeout 5 -s "$vartaspeicherip/cgi/ems_data.xml")


speicherwatt=$(echo $speicherwatttmp | grep 'P' | sed 's/.*value=//' |tr -d "'/>")
#wenn WR aus bzw. im standby (keine Antwort) ersetze leeren Wert durch eine 0
ra='^-?[0-9]+$'
if ! [[ $speicherwatt =~ $ra ]] ; then
		  speicherwatt="0"
fi

echo $speicherwatt > /var/www/html/openWB/ramdisk/speicherleistung

speichersoc=$(echo $speicherwatttmp | grep 'SOC' | sed 's/.*value=//' |tr -d "'/>")
if ! [[ $speichersoc =~ $ra ]] ; then
		  speichersoc="0"
fi


echo $speichersoc > /var/www/html/openWB/ramdisk/speichersoc

