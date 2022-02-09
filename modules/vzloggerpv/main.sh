#!/bin/bash

#Das Modul fragt einen VZlogger auf seinem eigenen Webserver ab und soll die Wattleistung als Ausgabe zurück geben
#Das pipen durch "jq" führt zeilenumbrüche ein.
#Mithilfe von sed wird die die gewünschte Zeile ausgewählt
#tr entfernt unnötige leerzeilen

watttmp=$(curl --connect-timeout 15 -s $vzloggerpvip)
watt=$(echo $watttmp | jq . | sed ''$vzloggerpvline'!d' | tr -d ' ' )
watt=$(echo "${watt}" | cut -f1 -d".")
if (( watt > 0 )); then
	watt=$((watt * -1 ))
fi
echo $watt
#zur weiteren verwendung im webinterface
echo $watt > /var/www/html/openWB/ramdisk/pvwatt
