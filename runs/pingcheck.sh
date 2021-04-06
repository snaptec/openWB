#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MYLOGFILE="$RAMDISKDIR/openWB.log"
DEBUG=$debug

DebugLog(){
	timestamp=`date +"%Y-%m-%d %H:%M:%S"`
	echo "$timestamp:  $@" >> $MYLOGFILE
}

#get Gateway for Connection
gateway=$(ip route get 1 | awk '{print $3;exit}')
if (( $DEBUG >= 1 )); then
	load=$(uptime |cut -d ' ' -f 13-15)
	DebugLog "Load: ${load}"
fi
#ping the gateway to see if the connection is OK
ping -c1 $gateway >/dev/null
ret=$?
if (( $ret != 0 )); then
	#get device
	mydevice=$(ip route get 1 |awk '{print $5;exit}')
	DebugLog "PING to Gateway ${gateway} with Device ${mydevice} Timed Out"
fi
