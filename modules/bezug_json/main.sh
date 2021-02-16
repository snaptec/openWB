#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
#DMOD="EVU"
DMOD="MAIN"
LOGFILE="$RAMDISKDIR/openWB.log"
Debug=$debug


#For development only
#Debug=1


openwbDebugLog ${DMOD} 1 "${bezugjsonwatt}"
openwbDebugLog ${DMOD} 1 "${bezugjsonkwh}"
openwbDebugLog ${DMOD} 1 "${einspeisungjsonkwh}"

answer=$(curl --connect-timeout 5 -s $bezugjsonurl)
evuwatt=$(echo $answer | jq -r "$bezugjsonwatt" | sed 's/\..*$//')
echo ${evuwatt}
openwbDebugLog  ${DMOD} 0 "Watt: ${evuwatt}"
echo $evuwatt > /var/www/html/openWB/ramdisk/wattbezug

if [ ! -z "${bezugjsonkwh}" ]; then
    evuikwh=$(echo $answer | jq -r "$bezugjsonkwh")
else
    evuikwh=0
fi

openwbDebugLog ${DMOD} 0 "BezugkWh: ${evuikwh}"
echo $evuikwh > /var/www/html/openWB/ramdisk/bezugkwh

if [ ! -z "${einspeisungjsonkwh}" ]; then
    evuekwh=$(echo $answer | jq -r "$einspeisungjsonkwh")
else
    evuekwh=0
fi
openwbDebugLog ${DMOD} 0 "EinspeiskWh: ${evuekwh}"
echo $evuekwh > /var/www/html/openWB/ramdisk/einspeisungkwh

