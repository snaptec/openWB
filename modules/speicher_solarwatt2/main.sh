#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULE="Speicher"
LOGFILE="$RAMDISKDIR/openWB.log"
Debug=$debug
myPid=$$

DebugLog(){
	if (( Debug > 0 )); then
		timestamp=`date +"%Y-%m-%d %H:%M:%S"`
		echo "$timestamp: ${MODULE}: $@" >> $LOGFILE
	fi
}


sresponse=$(curl --connect-timeout 3 -s "http://${speicher1_ip}:8080/")

ibat=$(echo $sresponse | jq '.FData.IBat') 
vbat=$(echo $sresponse | jq '.FData.VBat') 
speicherleistung=$(echo "($ibat * $vbat)" | bc) 
speicherleistung=$(echo "scale=0; ($speicherleistung) / (-1)" | bc) 

DebugLog "Speicherleistung: ${speicherleistung} W"
echo $speicherleistung > /var/www/html/openWB/ramdisk/speicherleistung 


speichersoc=$(echo $sresponse | jq '.SData.SoC' | sed 's/\..*$//') 

DebugLog "SpeicherSoC: ${speichersoc} %"
echo $speichersoc > /var/www/html/openWB/ramdisk/speichersoc 
