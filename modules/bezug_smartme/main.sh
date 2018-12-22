#!/bin/bash

#Variablen über die Weboberfläche abfragen und an das Modul übergeben.
bezug_smartme_user="user"
bezug_smartme_pass="pass"
bezug_smartme_url="https://smart-me.com:443/api/Devices/[ID]"

. /var/www/html/openWB/openwb.conf

#Daten einlesen
json=$(curl -u $bezug_smartme_user:$bezug_smartme_pass --connect-timeout 10 -s $bezug_smartme_url)

#Aktuelle Leistung (kW --> W)
wattbezug=$(echo $json | jq .ActivePower)
wattbezug=$(echo "scale=3 ; $wattbezug * 1000" | bc)
wattbezug=$(echo "$wattbezug / 1" | bc)

#Zählerstand Import(kWh)
ikwh=$(echo $json | jq .CounterReadingImport)
ikwh=$(echo "$ikwh / 1" | bc)

#Zählerstand Import(kWh)
ekwh=$(echo $json | jq .CounterReadingExport)
ekwh=$(echo "$ekwh / 1" | bc)

#Prüfen ob Werte gültig
re='^-?[0-9]+$'
if ! [[ $wattbezug =~ $re ]] ; then
	   wattbezug="0"
fi
if ! [[ $ikwh =~ $re ]] ; then
	   ikwh="0"
fi
if ! [[ $ekwh =~ $re ]] ; then
	   ekwh="0"
fi

#Ausgabe
echo $wattbezug
echo $wattbezug > /var/www/html/openWB/ramdisk/wattbezug
echo $ikwh > /var/www/html/openWB/ramdisk/bezugkwh
echo $ekwh > /var/www/html/openWB/ramdisk/einspeisungkwh
