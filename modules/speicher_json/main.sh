#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
#DMOD="BATT"
DMOD="MAIN"
#LOGFILE="$RAMDISKDIR/speicher.log"
#LOGFILE="$RAMDISKDIR/openWB.log"
Debug=$debug

#For Development only
#Debug=1

answer=$(curl --connect-timeout 5 -s $battjsonurl)
speicherleistung=$(echo $answer | jq -r "$battjsonwatt" | sed 's/\..*$//')
openwbDebugLog ${DMOD} 1 "BattLeistung: ${speicherleistung}"
echo ${speicherleistung}
echo $speicherleistung > /var/www/html/openWB/ramdisk/speicherleistung

if [ ! -z "$battjsonsoc" ]; then
	battsoc=$(echo $answer | jq -r "$battjsonsoc")
else
	battsoc=0
fi

openwbDebugLog ${DMOD} 1 "BattSoC: ${battsoc}"
echo $battsoc > /var/www/html/openWB/ramdisk/speichersoc
