#!/bin/bash

OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
#DMOD="PV"
DMOD="MAIN"

if [ $DMOD == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/wr_kostalpikomp.log"
fi

openwbDebugLog ${DMOD} 2 "PV IP: ${pvip}"

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "wr_kostalpikomp.kostal_piko_mp" "${pvip}" >>"$MYLOGFILE" 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

cat "$RAMDISKDIR/pvwatt"
