#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULE="PV"
LOGFILE="$RAMDISKDIR/openWB.log"
Debug=$debug

DebugLog(){
	if (( Debug > 0 )); then
		timestamp=`date +"%Y-%m-%d %H:%M:%S"`
		echo "$timestamp: ${MODULE}: $@" >> $LOGFILE
	fi
}

sresponse=$(curl --connect-timeout 3 -s "http://${speicher1_ip}/rest/kiwigrid/wizard/devices")

pvwatt=$(echo $sresponse | jq '.result.items | .[] | select(.tagValues.PowerProduced.value != null) | .tagValues.PowerProduced.value' | sed 's/\..*$//')
DebugLog "PV-Leistung: ${pvwatt} W"
pvwatt=$((pvwatt * -1))

echo $pvwatt > /var/www/html/openWB/ramdisk/pvwatt
echo $pvwatt
