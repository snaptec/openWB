#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULE="EVU"
LOGFILE="$RAMDISKDIR/openWB.log"
Debug=$debug
BEZUGFILE="$RAMDISKDIR/wattbezug"

DebugLog(){
	if (( Debug > 0 )); then
		timestamp=`date +"%Y-%m-%d %H:%M:%S"`
		echo "$timestamp: ${MODULE}: $@" >> $LOGFILE
	fi
}

if (( $solarwattmethod == 0 )); then 	#Abruf über Energy Manager
	sresponse=$(curl --connect-timeout 3 -s "http://${speicher1_ip}/rest/kiwigrid/wizard/devices")

	if ((${#sresponse}  < 10)); then
		bezugwatt=$(<$BEZUGFILE)
	else
		bezugw=$(echo $sresponse | jq '.result.items | .[] | select(.tagValues.PowerConsumedFromGrid.value != null) | .tagValues.PowerConsumedFromGrid.value' | sed 's/\..*$//')
		einspeisungw=$(echo $sresponse | jq '.result.items | .[] | select(.tagValues.PowerOut.value != null) | .tagValues.PowerOut.value' | head -n 1 | sed 's/\..*$//')
		bezugwatt=$(echo "scale=0; $bezugw - $einspeisungw /1" |bc)
	fi
fi
if (( $solarwattmethod == 1 )); then 	#Abruf über Gateway
	sresponse=$(curl --connect-timeout 3 -s "http://${speicher1_ip2}:8080/")

	if ((${#sresponse}  < 10)); then
		bezugwatt=$(<$BEZUGFILE)
	else
		bezugw=$(echo $sresponse | jq '.FData.PGrid' | sed 's/\..*$//')
		bezugwatt=$(echo "scale=0; $bezugw / 1" | bc)
	fi
fi

DebugLog "Netzbezug: $bezugwatt W"
echo $bezugwatt > $BEZUGFILE
echo $bezugwatt
