#!/bin/bash
OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
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

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.sma_shm.device" "counter" "${smashmbezugid}" >>"${MYLOGFILE}" 2>&1
ret=$?
openwbDebugLog ${DMOD} 2 "EVU RET: ${ret}"

wattbezug=$(<"${RAMDISKDIR}/wattbezug")
echo "$wattbezug"
