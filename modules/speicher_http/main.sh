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

openwbDebugLog ${DMOD} 2 "Speicher Export: ${speicherekwh_http}"
openwbDebugLog ${DMOD} 2 "Speicher Import: ${speicherikwh_http}"
openwbDebugLog ${DMOD} 2 "Speicher Watt: ${speicherleistung_http}"
openwbDebugLog ${DMOD} 2 "Speicher SoC: ${speichersoc_http}"

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.http.device" "bat" "${speicherleistung_http}" "${speicherikwh_http}" "${speicherekwh_http}" "${speichersoc_http}" >>"$MYLOGFILE" 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

speicherleistung=$(<"$RAMDISKDIR/speicherleistung")

openwbDebugLog ${DMOD} 1 "BattLeistung: ${speicherleistung}"
