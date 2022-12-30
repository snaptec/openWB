#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
#DMOD="EVU"
DMOD="MAIN"

if [ ${DMOD} == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/evu.log"
fi

openwbDebugLog ${DMOD} 2 "EVU URL: ${bezugjsonurl}"
openwbDebugLog ${DMOD} 2 "Filter Watt : ${bezugjsonwatt}"
openwbDebugLog ${DMOD} 2 "Filter Bezug: ${bezugjsonkwh}"
openwbDebugLog ${DMOD} 2 "Filter Einsp: ${einspeisungjsonkwh}"

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.json.device" "counter" "${bezugjsonurl}" "${bezugjsonwatt}" "${bezugjsonkwh}" "${einspeisungjsonkwh}" >>"$MYLOGFILE" 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

cat "${RAMDISKDIR}/wattbezug"
