#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"

#DMOD="MAIN"
DMOD="PV"

re='^-?[0-9]+$'

answer=$(curl -d "{\"801\":{\"170\":null}}" --connect-timeout 5 -s "$bezug2_solarlog_ip/getjp")

openwbDebugLog ${DMOD} 2 "answer: $answer"
pvwatt=$(echo "$answer" | jq '."801"."170"."101"' )
openwbDebugLog ${DMOD} 2 "pvwatt: $pvwatt"
pvkwh=$(echo "$answer" | jq '."801"."170"."109"' )
openwbDebugLog ${DMOD} 2 "pvkwh: $pvkwh"

if ! [[ $pvwatt =~ $re ]] ; then
	pvwatt="0"
	openwbDebugLog ${DMOD} 0 "pvwatt: NaN set 0"
fi

if (( pvwatt > 5 )); then
	pvwatt=$(echo "$pvwatt*-1" |bc)
fi
if ! [[ $pvkwh =~ $re ]] ; then
	openwbDebugLog ${DMOD} 2 "PVkWh: NaN get prev. Value"
	pvkwh=$(<"$RAMDISKDIR/pv2kwh")
fi

openwbDebugLog ${DMOD} 2 "pvwatt: $pvwatt"
openwbDebugLog ${DMOD} 2 "pvkwh: $pvkwh"
echo "$pvwatt"
echo "$pvwatt" > "$RAMDISKDIR/pv2watt"
echo "$pvkwh" > "$RAMDISKDIR/pv2kwh"
