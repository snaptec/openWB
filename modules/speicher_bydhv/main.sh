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

openwbDebugLog ${DMOD} 2 "Speicher IP: ${bydhvip}"
openwbDebugLog ${DMOD} 2 "Speicher Passwort: ${bydhvuser}"
openwbDebugLog ${DMOD} 2 "Speicher User: ${bydhvpass}"

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.byd.device" "bat" "${bydhvip}" "${bydhvuser}" "${bydhvpass}" >>"$MYLOGFILE" 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

speicherleistung=$(<"${RAMDISKDIR}/speicherleistung")

openwbDebugLog ${DMOD} 1 "BattLeistung: ${speicherleistung}"
