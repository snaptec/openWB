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
bash "$OPENWBBASEDIR/packages/legacy_run.sh" "wr_ethsdm120.readsdm120" "${wr_sdm120ip}" "${wr_sdm120id}" >>"$MYLOGFILE" 2>&1 
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"
cat "$RAMDISKDIR/pvwatt"
