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

openwbDebugLog ${DMOD} 2 "WR IP: ${wrfroniusip}"
openwbDebugLog ${DMOD} 2 "WR Erzeugung: ${froniuserzeugung}"
openwbDebugLog ${DMOD} 2 "WR Var2: ${froniusvar2}"
openwbDebugLog ${DMOD} 2 "WR IP2: ${wrfronius2ip}"
openwbDebugLog ${DMOD} 2 "WR Speicher: ${speichermodul}"

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.fronius.device" "counter_s0" "${wrfroniusip}" "${froniuserzeugung}" "${froniusvar2}" "${wrfronius2ip}">>"$MYLOGFILE" 2>&1

cat "${RAMDISKDIR}/wattbezug"
