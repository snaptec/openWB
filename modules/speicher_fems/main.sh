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

openwbDebugLog ${DMOD} 2 "Speicher IP: ${femsip}"
openwbDebugLog ${DMOD} 2 "Speicher Passwort: ${femskacopw}"
openwbDebugLog ${DMOD} 2 "Speicher Multi: ${multifems}"

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "speicher_fems.fems" "${multifems}" "${femskacopw}" "${femsip}" >>"${MYLOGFILE}" 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"
speicherleistung=$(<${RAMDISKDIR}/speicherleistung)
openwbDebugLog ${DMOD} 1 "BattLeistung: ${speicherleistung}"
