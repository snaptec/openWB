#!/bin/bash
OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULE="EVU"
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

bezugw=$(echo $sresponse | jq '.FData.PGrid' | sed 's/\..*$//')
bezugwatt=$(echo "scale=0; $bezugw / 1" | bc)

echo $bezugwatt > /var/www/html/openWB/ramdisk/wattbezug
echo $bezugwatt
DebugLog "Netzbezug: $bezugwatt W"
