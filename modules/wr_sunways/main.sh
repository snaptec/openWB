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

openwbDebugLog ${DMOD} 2 "PV IP: ${wrsunwaysip}"
openwbDebugLog ${DMOD} 2 "PV Passwort: ${wrsunwayspw}"

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.sunways.device" "inverter" "${wrsunwaysip}" "${wrsunwayspw}" "1">>"$MYLOGFILE" 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

cat "$RAMDISKDIR/pvwatt"
