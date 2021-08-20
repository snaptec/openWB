#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
DMOD="PV"
#DMOD="MAIN"
Debug=$debug

#For Development only
#Debug=1

if [ $DMOD == "MAIN" ]; then
	MYLOGFILE="$RAMDISKDIR/openWB.log"
else
	MYLOGFILE="$RAMDISKDIR/nurpv.log"
fi




openwbDebugLog ${DMOD} 2 "PV URL : ${wrjsonurl}"
openwbDebugLog ${DMOD} 2 "PV Watt: ${wrjsonwatt}"
openwbDebugLog ${DMOD} 2 "PV kWh : ${wrjsonkwh}"

python3 $OPENWBBASEDIR/modules/wr_json/read_json.py "${wrjsonurl}" "${wrjsonwatt}" "${wrjsonkwh}" "1" >>$MYLOGFILE 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

watt=$(<$RAMDISKDIR/pvwatt)
echo ${watt}


















#re='^[-+]?[0-9]+\.?[0-9]*$'
#answer=$(curl --connect-timeout 5 -s $wrjsonurl)
#pvwatt=$(echo $answer | jq -r "$wrjsonwatt" | sed 's/\..*$//')
## Wenn WR aus bzw. im Standby (keine Antwort), ersetze leeren Wert durch eine 0
#if ! [[ $pvwatt =~ $re ]] ; then
#	openwbDebugLog ${DMOD} 1 "PVWatt Not Numeric: $pvwatt . Check if Filter is correct or WR is in standby"
#	pvwatt=0
#fi
#
#if (( $pvwatt > 5 )); then
#	pvwatt=$(echo "$pvwatt*-1" |bc)
#fi	
#openwbDebugLog ${DMOD} 1 "PVWatt: ${pvwatt}"
#echo ${pvwatt}
#echo $pvwatt > /var/www/html/openWB/ramdisk/pvwatt
#
#if [ ! -z "$wrjsonkwh" ]; then
#	pvkwh=$(echo $answer | jq -r "$wrjsonkwh")
#	if ! [[ $pvkwh =~ $re ]] ; then
#		openwbDebugLog ${DMOD} 1 "PVkWh Not Numeric: $pvkwh . Check if Filter is correct or WR is in standby"
#		pvkwh=$(</var/www/html/openWB/ramdisk/pvkwh)
#	fi
#else
#	openwbDebugLog ${DMOD} 2 "PVkWh NoFilter is set"
#	pvkwh=0
#fi
#
#openwbDebugLog ${DMOD} 1 "PVkWh: ${pvkwh}"
#echo $pvkwh > /var/www/html/openWB/ramdisk/pvkwh
