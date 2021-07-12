#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
#DMOD="EVU"
DMOD="MAIN"
Debug=$debug

#For development only
#Debug=1

openwbDebugLog ${DMOD} 2 "${bezugjsonwatt}"
openwbDebugLog ${DMOD} 2 "${bezugjsonkwh}"
openwbDebugLog ${DMOD} 2 "${einspeisungjsonkwh}"

answer=$(curl --connect-timeout 5 -s $bezugjsonurl)
evuwatt=$(echo $answer | jq -r "$bezugjsonwatt" | sed 's/\..*$//')
echo ${evuwatt}
openwbDebugLog  ${DMOD} 1 "Watt: ${evuwatt}"
echo $evuwatt > /var/www/html/openWB/ramdisk/wattbezug

if [ ! -z "${bezugjsonkwh}" ]; then
	evuikwh=$(echo $answer | jq -r "$bezugjsonkwh")
else
	evuikwh=0
fi
openwbDebugLog ${DMOD} 1 "BezugkWh: ${evuikwh}"
echo $evuikwh > /var/www/html/openWB/ramdisk/bezugkwh

if [ ! -z "${einspeisungjsonkwh}" ]; then
	evuekwh=$(echo $answer | jq -r "$einspeisungjsonkwh")
else
	evuekwh=0
fi
openwbDebugLog ${DMOD} 1 "EinspeiskWh: ${evuekwh}"
echo $evuekwh > /var/www/html/openWB/ramdisk/einspeisungkwh
