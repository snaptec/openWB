#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
MODULEDIR=$(cd "$(dirname "$0")" && pwd)
DMOD="PV"
#DMOD="MAIN"
Debug=$debug

#For development only
#Debug=1

if [ ${DMOD} == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/nurpv.log"
fi

openwbDebugLog ${DMOD} 2 "PV KIT Version: ${pvflexversion}"
openwbDebugLog ${DMOD} 2 "PV IP: ${pvflexip}"
openwbDebugLog ${DMOD} 2 "PV Port : ${pvflexport}"
openwbDebugLog ${DMOD} 2 "PV ID : ${pvflexid}"

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.openwb_flex.device" "inverter" "${pvflexversion}" "${pvflexip}" "${pvflexport}" "${pvflexid}" "1" >>"$MYLOGFILE" 2>&1
cat "$RAMDISKDIR/pvwatt"
