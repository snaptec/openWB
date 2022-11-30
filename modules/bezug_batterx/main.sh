#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
DMOD="MAIN"

#For development only
#Debug=1

if [ ${DMOD} == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/evu.log"
fi

# Werte werden im WR ausgelesen, max eine Abfrage pro Sekunde
if [ ${pvwattmodul} != "wr_batterx" ]; then
	bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.batterx.device" "counter" "${batterx_ip}" >>"$MYLOGFILE" 2>&1
	ret=$?
fi

openwbDebugLog ${DMOD} 2 "EVU RET: ${ret}"
cat "${RAMDISKDIR}/wattbezug"
