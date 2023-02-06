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

openwbDebugLog ${DMOD} 2 "Speicher IP-Adresse: ${batterx_ip}"

# Werte werden im WR ausgelesen, max eine Abfrage pro Sekunde
if [ ${pvwattmodul} != "wr_batterx" ]; then
	bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.batterx.device" "bat" "${batterx_ip}" >>"$MYLOGFILE" 2>&1
	ret=$?
	openwbDebugLog ${DMOD} 2 "RET: ${ret}"
fi

speicherleistung=$(<"${RAMDISKDIR}"/speicherleistung)

openwbDebugLog ${DMOD} 1 "BattLeistung: ${speicherleistung}"
