#!/bin/bash

OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
DMOD="PV"
#DMOD="MAIN"

if [ $DMOD == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/nurpv.log"
fi

openwbDebugLog ${DMOD} 2 "SMA serials: ${smaemdpvid}"

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.sma_shm.device" "inverter" "${smaemdpvid}" "1">>"$MYLOGFILE" 2>&1
ret=$?
openwbDebugLog ${DMOD} 2 "EVU RET: ${ret}"

cat "$RAMDISKDIR/pvwatt"
