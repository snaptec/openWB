#!/bin/bash

#Das Modul fragt einen VZlogger auf seinem eigenen Webserver ab und soll die Wattleistung als Ausgabe zurück geben
#Das pipen durch "jq" führt zeilenumbrüche ein.
#Mithilfe von sed wird die die gewünschte Zeile ausgewählt
#tr entfernt unnötige leerzeilen

#IP und Port des VZlogger
ip=10.20.0.51:8080


watttmp=$(curl --connect-timeout 15 -s $ip)
watt=$(echo $watttmp | jq . | sed '13!d' | tr -d ' ' )
echo $watt
#zur weiteren verwendung im webinterface
echo $watt > /var/run/wattbezug
