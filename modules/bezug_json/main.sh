#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
LOGFILE="$RAMDISKDIR/evu.log"
Debug=$debug
myPid=$$


#For development only
Debug=1

DebugLog(){
        if (( Debug > 0 )); then
                timestamp=`date +"%Y-%m-%d %H:%M:%S"`
                if (( Debug == 2 )); then
                      echo "$timestamp: PID:$myPid: $@" >> $LOGFILE
                else
                      echo "$timestamp: $@" >> $LOGFILE
                fi
        fi
}


DebugLog $bezugjsonwatt
DebugLog $bezugjsonkwh
DebugLog $einspeisungjsonkwh

answer=$(curl --connect-timeout 5 -s $bezugjsonurl)
evuwatt=$(echo $answer | jq -r "$bezugjsonwatt" | sed 's/\..*$//')
echo ${evuwatt}
DebugLog "Watt: ${evuwatt}"
echo $evuwatt > /var/www/html/openWB/ramdisk/wattbezug
evuikwh=$(echo $answer | jq -r "$bezugjsonkwh")
DebugLog "BezugkWh: ${evuikwh}"
echo $evuikwh > /var/www/html/openWB/ramdisk/bezugkwh
evuekwh=$(echo $answer | jq -r "$einspeisungjsonkwh")
DebugLog "EinspeiskWh: ${evuekwh}"
echo $evuekwh > /var/www/html/openWB/ramdisk/einspeisungkwh

