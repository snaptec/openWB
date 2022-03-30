#!/bin/bash

OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
#DMOD="BATT"
DMOD="MAIN"

if [ ${DMOD} == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/speicher.log"
fi

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "speicher_kostalplenticore.kostal_plenticore" >>"${MYLOGFILE}" 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"
speicherleistung=$(<"${RAMDISKDIR}/speicherleistung")
openwbDebugLog ${DMOD} 1 "BattLeistung: ${speicherleistung}"
