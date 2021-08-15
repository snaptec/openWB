#!/bin/bash

#Das Modul fragt einen VZlogger auf seinem eigenen Webserver ab und soll die Wattleistung als Ausgabe zurück geben
#Das pipen durch "jq" führt zeilenumbrüche ein.
#Mithilfe von sed wird die die gewünschte Zeile ausgewählt
#tr entfernt unnötige leerzeilen

watttmp=$(curl --connect-timeout 15 -s $vzloggerip)
watt=$(echo $watttmp | jq . | sed ''$vzloggerline'!d' | tr -d ' ' )
watt=$(echo "${watt}" | cut -f1 -d".")
echo $watt
#zur weiteren verwendung im webinterface
echo $watt > /var/www/html/openWB/ramdisk/wattbezug

kwh=$(echo $watttmp | jq . | sed ''$vzloggerkwhline'!d' | tr -d ' ' |tr -d '\n' )
echo $kwh > /var/www/html/openWB/ramdisk/bezugkwh
ekwh=$(echo $watttmp | jq . | sed ''$vzloggerekwhline'!d' | tr -d ' ' |tr -d '\n' )
echo $ekwh > /var/www/html/openWB/ramdisk/einspeisungkwh
