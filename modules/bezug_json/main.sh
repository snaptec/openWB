#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
MODULE="EVU"
LOGFILE="$RAMDISKDIR/openWB.log"
Debug=$debug
myPid=$$


#For development only
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


DebugLog "${bezugjsonwatt}"
DebugLog "${bezugjsonkwh}"
DebugLog "${einspeisungjsonkwh}"

answer=$(curl --connect-timeout 5 -s $bezugjsonurl)
evuwatt=$(echo $answer | jq -r "$bezugjsonwatt" | sed 's/\..*$//')
echo ${evuwatt}
DebugLog "Watt: ${evuwatt}"
echo $evuwatt > /var/www/html/openWB/ramdisk/wattbezug

if [ ! -z "${bezugjsonkwh}" ]; then
    evuikwh=$(echo $answer | jq -r "$bezugjsonkwh")
    DebugLog "BezugkWh: ${evuikwh}"
else
    evuikwh=0
    DebugLog "BezugkWh: ${evuikwh}"
fi
echo $evuikwh > /var/www/html/openWB/ramdisk/bezugkwh

if [ ! -z "${einspeisungjsonkwh}" ]; then
    evuekwh=$(echo $answer | jq -r "$einspeisungjsonkwh")
    DebugLog "EinspeiskWh: ${evuekwh}"
else
    evuekwh=0
    DebugLog "EinspeiskWh: ${evuekwh}"
fi
echo $evuekwh > /var/www/html/openWB/ramdisk/einspeisungkwh

