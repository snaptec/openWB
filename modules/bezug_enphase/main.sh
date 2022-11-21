#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
#DMOD="EVU"
DMOD="MAIN"

if [ ${DMOD} == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/evu.log"
fi

openwbDebugLog ${DMOD} 2 "Envoy IP/Hostname: ${wrenphasehostname}"
openwbDebugLog ${DMOD} 2 "Zaehler EID: ${bezugenphaseeid}"

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.enphase.device" "counter" "${wrenphasehostname}" "${bezugenphaseeid}" >>"$MYLOGFILE" 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

cat "${RAMDISKDIR}/wattbezug"
