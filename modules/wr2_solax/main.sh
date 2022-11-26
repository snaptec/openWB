#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
#DMOD="PV"
DMOD="MAIN"

if [ ${DMOD} == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/nurpv.log"
fi

openwbDebugLog ${DMOD} 2 "PV2 IP: ${pv2ip}"

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.solax.device" "inverter" "${pv2ip}" "0" "2" >>"$MYLOGFILE" 2>&1

cat "$RAMDISKDIR/pv2watt"
