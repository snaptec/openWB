#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MYLOGFILE="$RAMDISKDIR/openWB.log"


DebugLog(){
		timestamp=`date +"%Y-%m-%d %H:%M:%S"`
		echo "$timestamp:  $@" >> $MYLOGFILE
}

#DebugLog "Ping Test"

#get Gateway for Connection
gateway=$(ip route get 1 | awk '{print $3;exit}')

#ping the gateway to see if the connection is OK
ping -c1 $gateway >/dev/null
ret=$?
if (( $ret != 0 )); then
        #get device
	mydevice=$(ip route get 1 |awk '{print $5;exit}')
	DebugLog "PING to Gateway ${gateway} with Device ${mydevice} Timed Out"
fi

