#!/bin/bash

OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
DMOD="PV"
#DMOD="MAIN"
Debug=$debug

#For Development only
#Debug=1

if [ ${DMOD} == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/nurpv.log"
fi

openwbDebugLog ${DMOD} 2 "PV URL : ${wr2jsonurl}"
openwbDebugLog ${DMOD} 2 "PV Watt: ${wr2jsonwatt}"
openwbDebugLog ${DMOD} 2 "PV kWh : ${wr2jsonkwh}"

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.json.device" "inverter" "${wr2jsonurl}" "${wr2jsonwatt}" "${wr2jsonkwh}" "2" >>"$MYLOGFILE" 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

cat "${RAMDISKDIR}/pv2watt"
