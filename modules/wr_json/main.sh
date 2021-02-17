#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
DMOD="PV"
#DMOD="MAIN"
#LOGFILE="$RAMDISKDIR/pv_wr.log"
#LOGFILE="$RAMDISKDIR/openWB.log"
Debug=$debug

#For Development only
#Debug=1


answer=$(curl --connect-timeout 5 -s $wrjsonurl)
pvwatt=$(echo $answer | jq -r "$wrjsonwatt" | sed 's/\..*$//')
	if (( $pvwatt > 5 )); then
		pvwatt=$(echo "$pvwatt*-1" |bc)
	fi	
openwbDebugLog ${DMOD} 1 "PVWatt: ${pvwatt}"
echo ${pvwatt}
echo $pvwatt > /var/www/html/openWB/ramdisk/pvwatt

if [ ! -z "$wrjsonkwh" ]; then
    pvkwh=$(echo $answer | jq -r "$wrjsonkwh")
else
    pvkwh=0
fi

openwbDebugLog ${DMOD} 1 "PVkWh: ${pvkwh}"
echo $pvkwh > /var/www/html/openWB/ramdisk/pvkwh
