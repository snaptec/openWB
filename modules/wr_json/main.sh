#!/bin/bash

OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
DMOD="PV"
#DMOD="MAIN"
Debug=$debug

#For Development only
#Debug=1

if [ $DMOD == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/nurpv.log"
fi

openwbDebugLog ${DMOD} 2 "PV URL : ${wrjsonurl}"
openwbDebugLog ${DMOD} 2 "PV Watt: ${wrjsonwatt}"
openwbDebugLog ${DMOD} 2 "PV kWh : ${wrjsonkwh}"

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.json.device" "inverter" "${wrjsonurl}" "${wrjsonwatt}" "${wrjsonkwh}" "1" >>"$MYLOGFILE" 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

cat "${RAMDISKDIR}/pvwatt"
