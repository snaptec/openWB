#!/bin/bash

. /var/www/html/openWB/openwb.conf

#Daten einlesen
json=$(curl -u $wr_smartme_user:$wr_smartme_pass --connect-timeout 10 -s $wr_smartme_url)

#Aktuelle Leistung (kW --> W)
wattwr=$(echo $json | jq .ActivePower)
wattwr=$(echo "scale=3 ; $wattwr * 1000" | bc)
wattwr=$(echo "$wattwr / 1" | bc)

#Zählerstand Export (kWh --> Wh)
pvkwh=$(echo $json | jq .CounterReadingExport)
pvkwh=$(echo "scale=3 ; $pvkwh * 1000" | bc)
#Zur Reduzierung der Datenmenge kann die folgende Zeile eingefügt werden.
#pvkwh=$(echo "$pvkwh / 1" | bc)

#Prüfen ob Werte gültig
re='^[-+]?[0-9]+\.?[0-9]*$'
if ! [[ $wattwr =~ $re ]] ; then
	   wattwr=$(</var/www/html/openWB/ramdisk/pvwatt)
fi
if ! [[ $pvkwh =~ $re ]] ; then
	   pvkwh=$(</var/www/html/openWB/ramdisk/pvkwh)
fi

#Ausgabe
echo $wattwr
echo $wattwr > /var/www/html/openWB/ramdisk/pvwatt

#WR-AC-Leistung muss in andere Datei für Berechnung Hausverbrauch
#zunächst hier den gleichen Wert wie für pvwatt nehmen bis Modul angepasst ist
echo $wattwr > /var/www/html/openWB/ramdisk/wracwatt

echo $pvkwh > /var/www/html/openWB/ramdisk/pvkwh

pvkwhk=$(echo "scale=3 ; $pvkwh / 1000" | bc)
echo $pvkwhk > /var/www/html/openWB/ramdisk/pvkwhk
