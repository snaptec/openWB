#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
MODULE="BATT"
#LOGFILE="$RAMDISKDIR/speicher.log"
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



answer=$(curl --connect-timeout 5 -s $battjsonurl)
speicherleistung=$(echo $answer | jq -r "$battjsonwatt" | sed 's/\..*$//')
DebugLog "BattLeistung: ${speicherleistung}"
echo ${speicherleistung}
echo $speicherleistung > /var/www/html/openWB/ramdisk/speicherleistung

if [ ! -z "$battjsonsoc" ]; then
    battsoc=$(echo $answer | jq -r "$battjsonsoc")
    DebugLog "BattSoC: ${battsoc}"
else
    battsoc=0
    DebugLog "BattSoC: ${battsoc}"
fi

echo $battsoc > /var/www/html/openWB/ramdisk/speichersoc
