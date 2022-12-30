#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
#DMOD="EVU"
DMOD="MAIN"

#For development only
#Debug=1

if [ ${DMOD} == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/evu.log"
fi

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.good_we.device" "counter" "${good_we_ip}" "${good_we_id}">>"$MYLOGFILE" 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "EVU RET: ${ret}"
cat "${RAMDISKDIR}/wattbezug"
