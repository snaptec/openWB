#!/bin/bash

#Daten einlesen
json=$(curl -s -u $bezug_smartme_user:$bezug_smartme_pass --connect-timeout 10 -s $bezug_smartme_url)

#Aktuelle Leistung (kW --> W)
wattbezug=$(echo $json | jq .ActivePower)
wattbezug=$(echo "scale=3 ; $wattbezug * 1000" | bc)
wattbezug=$(echo "$wattbezug / 1" | bc)

wattbezug1=$(echo $json | jq .ActivePowerL1)
wattbezug1=$(echo "scale=3 ; $wattbezug1 * 1000" | bc)
wattbezug1=$(echo "$wattbezug1 / 1" | bc)

wattbezug2=$(echo $json | jq .ActivePowerL2)
wattbezug2=$(echo "scale=3 ; $wattbezug2 * 1000" | bc)
wattbezug2=$(echo "$wattbezug2 / 1" | bc)

wattbezug3=$(echo $json | jq .ActivePowerL3)
wattbezug3=$(echo "scale=3 ; $wattbezug3 * 1000" | bc)
wattbezug3=$(echo "$wattbezug3 / 1" | bc)

if [ $wattbezug1 = '0' ] ; then
	wattbezug1=$wattbezug
fi

#Zählerstand Import(kWh)
ikwh=$(echo $json | jq .CounterReadingImport)
ikwh=$(echo "scale=3 ; $ikwh * 1000" | bc)
#Zur Reduzierung der Datenmenge kann die folgende Zeile eingefügt werden.
#ikwh=$(echo "$ikwh / 1" | bc) 

#Zählerstand Export(kWh)
ekwh=$(echo $json | jq .CounterReadingExport)
ekwh=$(echo "scale=3 ; $ekwh * 1000" | bc)
#Zur Reduzierung der Datenmenge kann die folgende Zeile eingefügt werden.
#ekwh=$(echo "$ekwh / 1" | bc)

#Weitere Zählerdaten für die Statusseite (PowerFaktor, Spannung und Strom)
evupf1=$(echo $json | jq .PowerFactorL1)
evupf2=$(echo $json | jq .PowerFactorL2)
evupf3=$(echo $json | jq .PowerFactorL3)
evuv1=$(echo $json | jq .VoltageL1)
evuv2=$(echo $json | jq .VoltageL2)
evuv3=$(echo $json | jq .VoltageL3)
bezuga1=$(echo $json | jq .CurrentL1)
bezuga2=$(echo $json | jq .CurrentL2)
bezuga3=$(echo $json | jq .CurrentL3)
if [ $bezuga1 = 'null' ] ; then
	bezuga1=$(echo $json | jq .Current)
fi

#Prüfen ob Werte gültig
re='^[-+]?[0-9]+\.?[0-9]*$'
if ! [[ $wattbezug =~ $re ]] ; then
	wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
fi
if ! [[ $ikwh =~ $re ]] ; then
	ikwh=$(</var/www/html/openWB/ramdisk/bezugkwh)
fi
if ! [[ $ekwh =~ $re ]] ; then
	ekwh=$(</var/www/html/openWB/ramdisk/einspeisungkwh)
fi

#Ausgabe
echo $wattbezug
echo $wattbezug > /var/www/html/openWB/ramdisk/wattbezug
echo $wattbezug1 > /var/www/html/openWB/ramdisk/bezugw1
echo $wattbezug2 > /var/www/html/openWB/ramdisk/bezugw2
echo $wattbezug3 > /var/www/html/openWB/ramdisk/bezugw3
echo $ikwh > /var/www/html/openWB/ramdisk/bezugkwh
echo $ekwh > /var/www/html/openWB/ramdisk/einspeisungkwh
echo $evupf1 > /var/www/html/openWB/ramdisk/evupf1
echo $evupf2 > /var/www/html/openWB/ramdisk/evupf2
echo $evupf3 > /var/www/html/openWB/ramdisk/evupf3
echo $evuv1 > /var/www/html/openWB/ramdisk/evuv1
echo $evuv2 > /var/www/html/openWB/ramdisk/evuv2
echo $evuv3 > /var/www/html/openWB/ramdisk/evuv3
echo $bezuga1 > /var/www/html/openWB/ramdisk/bezuga1
echo $bezuga2 > /var/www/html/openWB/ramdisk/bezuga2
echo $bezuga3 > /var/www/html/openWB/ramdisk/bezuga3
