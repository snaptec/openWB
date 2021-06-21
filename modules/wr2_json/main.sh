#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
DMOD="PV"
#DMOD="MAIN"
#LOGFILE="$RAMDISKDIR/pv_wr.log"
#LOGFILE="$RAMDISKDIR/openWB.log"
Debug=$debug

#For Development only
#Debug=1


re='^[-+]?[0-9]+\.?[0-9]*$'
answer=$(curl --connect-timeout 5 -s $wr2jsonurl)
pvwatt=$(echo $answer | jq -r "$wr2jsonwatt" | sed 's/\..*$//')
# Wenn WR aus bzw. im Standby (keine Antwort), ersetze leeren Wert durch eine 0
if ! [[ $pvwatt =~ $re ]] ; then
	openwbDebugLog ${DMOD} 1 "PV2Watt Not Numeric: $pvwatt . Check if Filter is correct or WR is in standby"
	pvwatt=0
fi

if (( $pvwatt > 5 )); then
	pvwatt=$(echo "$pvwatt*-1" |bc)
fi

openwbDebugLog ${DMOD} 1 "PV2Watt: ${pvwatt}"
echo ${pvwatt}
#if ! [[ $pvwatt =~ $re ]] ; then
#	   pvwatt=$(</var/www/html/openWB/ramdisk/pv2watt)
#fi
echo $pvwatt > /var/www/html/openWB/ramdisk/pv2watt
pv2kwh=$(echo $answer | jq -r "$wr2jsonkwh")
if ! [[ $pv2kwh =~ $re ]] ; then
	   pv2kwh=$(</var/www/html/openWB/ramdisk/pv2kwh)
fi

echo $pv2kwh > /var/www/html/openWB/ramdisk/pv2kwh
openwbDebugLog ${DMOD} 1 "PV2kWh: ${pv2kwh}"
