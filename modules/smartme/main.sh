#!/bin/bash
#Variablen über die Weboberfläche abfragen und an das Modul übergeben.
wr_smartme_user="user"
wr_smartme_pass="password"
wr_smartme_url="https://smart-me.com:443/api/Devices/[Device_ID]"

. /var/www/html/openWB/openwb.conf

#Daten einlesen
json=$(curl -u $wr_smartme_user:$wr_smartme_pass --connect-timeout 10 -s $wr_smartme_url)

#Aktuelle PV Leistung (W)
wattwr=$(echo $json | jq .ActivePower)
wattwr=$(echo "scale=3 ; $wattwr * 1000" | bc)
wattwr=$(echo "$wattwr / 1" | bc)

#Zählerstand PV (kWh)
pvkwh=$(echo $json | jq .CounterReading)
pvkwh=$(echo "$pvkwh / -1" | bc)

#Prüfen ob Werte gültig
re='^-?[0-9]+$'
if ! [[ $wattwr =~ $re ]] ; then
	   wattwr="0"
fi
if ! [[ $pvkwh =~ $re ]] ; then
	   pvkwh="0"
fi

#Ausgabe
echo $wattwr
echo $wattwr > /var/www/html/openWB/ramdisk/pvwatt
echo $pvkwh > /var/www/html/openWB/ramdisk/pvkwh

pvkwhk=$(echo "scale=3 ; $pvkwh / 1000" | bc)
echo $pvkwhk > /var/www/html/openWB/ramdisk/pvkwhk
