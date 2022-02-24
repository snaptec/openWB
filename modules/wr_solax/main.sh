#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
DMOD="PV"
#DMOD="MAIN"

if [ ${DMOD} == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/nurpv.log"
fi

openwbDebugLog ${DMOD} 2 "PV IP: ${solaxip}"

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.solax.device" "inverter" "${solaxip}" "1">>"$MYLOGFILE" 2>&1

cat "$RAMDISKDIR/pvwatt"
