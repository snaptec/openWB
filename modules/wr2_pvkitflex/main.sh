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

openwbDebugLog ${DMOD} 2 "PV KIT Version: ${pv2flexversion}"
openwbDebugLog ${DMOD} 2 "PV IP: ${pv2flexip}"
openwbDebugLog ${DMOD} 2 "PV Port : ${pv2flexport}"
openwbDebugLog ${DMOD} 2 "PV ID : ${pv2flexid}"

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.openwb_flex.device" "inverter" "${pv2flexversion}" "${pv2flexip}" "${pv2flexport}" "${pv2flexid}" "2">>"$MYLOGFILE" 2>&1

cat "$RAMDISKDIR/pv2watt"
