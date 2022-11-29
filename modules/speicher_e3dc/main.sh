#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
#DMOD="BAT"
DMOD="MAIN"

if [ ${DMOD} == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/bat.log"
fi

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.e3dc.device" "bat" "$e3dcip" "$e3dc2ip" "$e3dcextprod" "$pvwattmodul" "1" >>"$MYLOGFILE" 2>&1
ret=$?

openwbDebugLog "${DMOD}" 2 "BAT RET: ${ret}"
