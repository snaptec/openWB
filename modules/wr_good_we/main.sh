#!/bin/bash

OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
DMOD="PV"

#For Development only
#Debug=1

if [ $DMOD == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/nurpv.log"
fi

openwbDebugLog ${DMOD} 2 "WR IP: ${good_we_ip}"
openwbDebugLog ${DMOD} 2 "WR ID: ${good_we_id}"

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.good_we.device" "inverter" "${good_we_ip}" "${good_we_id}" "1" >>"$MYLOGFILE" 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"
cat "${RAMDISKDIR}/pvwatt"
