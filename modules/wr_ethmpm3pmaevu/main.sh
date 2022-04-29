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

if [[ $wattbezugmodul != "bezug_ethmpm3pm" ]]; then
	bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.openwb.device" "evu_inverter" "${pvkitversion}" "1">>"$MYLOGFILE" 2>&1
else
	bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.openwb.device" "evu_inverter" "${pvkitversion}" "1" "${evukitversion}">>"$MYLOGFILE" 2>&1
fi
cat "$RAMDISKDIR/pvwatt"
