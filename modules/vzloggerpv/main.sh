#!/bin/bash

#Das Modul fragt einen VZlogger auf seinem eigenen Webserver ab und soll die Wattleistung als Ausgabe zurück geben
#Das pipen durch "jq" führt zeilenumbrüche ein.
#Mithilfe von sed wird die die gewünschte Zeile ausgewählt
#tr entfernt unnötige leerzeilen
. /var/www/html/openWB/openwb.conf


pvwatttmp=$(curl --connect-timeout 15 -s $vzloggerpvip)
pvwatt=$(echo $pvwatttmp | jq . | sed ''$vzloggerpvline'!d' | tr -d ' ' )
pvwatt=$(echo "${watt}" | cut -f1 -d".")
echo $pvwatt
#zur weiteren verwendung im webinterface
echo $pvwatt > /var/www/html/openWB/ramdisk/pvwatt
