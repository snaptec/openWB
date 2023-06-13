#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
DMOD="PV"

#For Development only
#Debug=1

if [ $DMOD == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/nurpv.log"
fi

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.fems.device" "inverter" "${femsip}" "${femskacopw}" "0" "1">>"${MYLOGFILE}" 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"
cat "${RAMDISKDIR}/pvwatt"

