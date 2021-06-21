#!/bin/bash

#Auslesen vom S0-Eingang eines Youless LS120 Energy Monitor.

answer=$(curl --connect-timeout 5 -s $wryoulessip/a?f=j)

#aktuelle Ausgangsleistung am WR [W]
pvwatt=$(echo $answer | jq -r '.ps0' | sed 's/\..*$//')
if (( $pvwatt > 5 )); then
	pvwatt=$(echo "$pvwatt*-1" |bc)
fi
echo $pvwatt
echo $pvwatt > /var/www/html/openWB/ramdisk/pvwatt
#Gesamtz‰hlerstand am WR [Wh]
pvkwh=$(echo $answer | jq -r '.cs0' | sed 's/,//g')
echo $pvkwh > /var/www/html/openWB/ramdisk/pvkwh
#Gesamtz‰hlerstand am WR [kWh]
pvkwh=$(echo "$pvkwh/1000" |bc)
echo $pvkwh > /var/www/html/openWB/ramdisk/pvkwhk
