#!/bin/bash

OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
DMOD="MAIN"

#For Development only
#Debug=1

if [ ${DMOD} == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/speicher.log"
fi

if [[ "$sbs25se" == "1" ]]; then
	bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.sma_sunny_boy.device" "bat_smart_energy" "${sbs25ip}" >>"$MYLOGFILE" 2>&1
else
	bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.sma_sunny_boy.device" "bat" "${sbs25ip}" >>"$MYLOGFILE" 2>&1
fi
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

speicherleistung=$(<"${RAMDISKDIR}"/speicherleistung)

openwbDebugLog ${DMOD} 1 "BattLeistung: ${speicherleistung}"
