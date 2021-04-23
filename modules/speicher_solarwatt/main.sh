#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULE="Speicher"
LOGFILE="$RAMDISKDIR/openWB.log"
Debug=$debug

DebugLog(){
	if (( Debug > 0 )); then
		timestamp=`date +"%Y-%m-%d %H:%M:%S"`
		echo "$timestamp: ${MODULE}: $@" >> $LOGFILE
	fi
}

if (( $solarwattmethod == 0 )); then 	#Abruf über Energy Manager
	sresponse=$(curl --connect-timeout 5 -s "http://${speicher1_ip}/rest/kiwigrid/wizard/devices")

	if ((${#sresponse}  < 10)); then
		exit 1
	fi
	
	speichere=$(echo $sresponse | jq '.result.items | .[] | select(.tagValues.PowerConsumedFromStorage.value != null) | .tagValues.PowerConsumedFromStorage.value' | sed 's/\..*$//')
	speicherein=$(echo $sresponse | jq '.result.items | .[] | select(.tagValues.PowerOutFromStorage.value != null) | .tagValues.PowerOutFromStorage.value' | sed 's/\..*$//') 
	speicheri=$(echo $sresponse | jq '.result.items | .[] | select(.tagValues.PowerBuffered.value != null) | .tagValues.PowerBuffered.value' | sed 's/\..*$//') 

	speicherleistung=$(echo "scale=0; ($speichere + $speicherin - $speicheri) *-1" | bc) 
	speichersoc=$(echo $sresponse | jq '.result.items | .[] | select(.tagValues.StateOfCharge.value != null) | .tagValues.StateOfCharge.value' | sed 's/\..*$//') 
fi

if (( $solarwattmethod == 1 )); then 	#Abruf über Gateway
	sresponse=$(curl --connect-timeout 3 -s "http://${speicher1_ip2}:8080/")

	if ((${#sresponse}  < 10)); then
		exit 1
	fi
	
	ibat=$(echo $sresponse | jq '.FData.IBat') 
	vbat=$(echo $sresponse | jq '.FData.VBat') 
	speicherleistung=$(echo "($ibat * $vbat)" | bc) 
	speicherleistung=$(echo "scale=0; ($speicherleistung) / (-1)" | bc)
	speichersoc=$(echo $sresponse | jq '.SData.SoC' | sed 's/\..*$//')
fi

DebugLog "Speicherleistung: ${speicherleistung} W"
echo $speicherleistung > /var/www/html/openWB/ramdisk/speicherleistung 

DebugLog "SpeicherSoC: ${speichersoc} %"
echo $speichersoc > /var/www/html/openWB/ramdisk/speichersoc 
