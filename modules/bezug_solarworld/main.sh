#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
#DMOD="EVU"
DMOD="MAIN"

if [ $DMOD == "MAIN" ]; then
	MYLOGFILE="$RAMDISKDIR/openWB.log"
else
	MYLOGFILE="$RAMDISKDIR/bezug_solarworld.log"
fi

openwbDebugLog ${DMOD} 2 "Bezug Solarworld IP: ${solarworld_emanagerip}"

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.solar_world.device" "counter" "${solarworld_emanagerip}" >>"$MYLOGFILE" 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"
cat "${RAMDISKDIR}/wattbezug"
