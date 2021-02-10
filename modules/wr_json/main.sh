#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
MODULE="PV"
#LOGFILE="$RAMDISKDIR/pv_wr.log"
LOGFILE="$RAMDISKDIR/openWB.log"
Debug=$debug
myPid=$$

#For Development only
#Debug=1

DebugLog(){
        if (( Debug > 0 )); then
                timestamp=`date +"%Y-%m-%d %H:%M:%S"`
                if (( Debug == 2 )); then
                      echo "$timestamp: ${MODULE}: PID:$myPid: $@" >> $LOGFILE
                else
                      echo "$timestamp: ${MODULE}: $@" >> $LOGFILE
                fi
        fi
}



answer=$(curl --connect-timeout 5 -s $wrjsonurl)
pvwatt=$(echo $answer | jq -r "$wrjsonwatt" | sed 's/\..*$//')
	if (( $pvwatt > 5 )); then
		pvwatt=$(echo "$pvwatt*-1" |bc)
	fi	
DebugLog "PVWatt: ${pvwatt}"
echo ${pvwatt}
echo $pvwatt > /var/www/html/openWB/ramdisk/pvwatt
pvkwh=$(echo $answer | jq -r "$wrjsonkwh")
DebugLog "PVkWh: ${pvkwh}"
echo $pvkwh > /var/www/html/openWB/ramdisk/pvkwh
