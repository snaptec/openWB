#!/bin/bash

OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
#DMOD="BATT"
DMOD="MAIN"

if [ ${DMOD} == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/bat.log"
fi

# Auslesen eines Varta Speicher über die integrierte XML-API der Batteroe.

if [[ "$usevartamodbus" != "1" ]]; then
	bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.varta.device" "bat_api" "${vartaspeicherip}">>"$MYLOGFILE" 2>&1
else 
	bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.varta.device" "bat_modbus" "${vartaspeicherip}" "${vartaspeicher2ip}" >>"$MYLOGFILE" 2>&1
fi
ret=$?
openwbDebugLog ${DMOD} 2 "RET: ${ret}"
