#!/bin/bash

OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
#DMOD="EVU"
DMOD="MAIN"

if [ $DMOD == "MAIN" ]; then
	MYLOGFILE="$RAMDISKDIR/openWB.log"
else
	MYLOGFILE="$RAMDISKDIR/bezug_smartme.log"
fi

openwbDebugLog ${DMOD} 2 "Bezug Solarwatt Methode: ${solarwattmethod}"
openwbDebugLog ${DMOD} 2 "Bezug Solarwatt IP1 : ${speicher1_ip}"
openwbDebugLog ${DMOD} 2 "Bezug Solarwatt IP2: ${speicher1_ip2}"

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.solar_watt.device" "counter" "${speicher1_ip}" "${speicher1_ip2}" "${solarwattmethod}" >>"$MYLOGFILE" 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

cat "${RAMDISKDIR}/wattbezug"
