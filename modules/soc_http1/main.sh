#!/bin/bash

#Soc from http

hsoc=$(curl --connect-timeout 15 -s $hsocip1 | cut -f1 -d".")

#wenn SOC nicht verfügbar (keine Antwort) ersetze leeren Wert durch eine 0
re='^[0-9]+$'
if ! [[ $hsoc =~ $re ]] ; then
   hsoc="0"
fi
#echo $hsoc
#zur weiteren verwendung im webinterface
echo $hsoc > /var/www/html/openWB/ramdisk/soc1
