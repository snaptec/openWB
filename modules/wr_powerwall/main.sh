#!/bin/bash

OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
DMOD="MAIN"

if [ $DMOD == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/wr_powerwall.log"
fi

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.tesla.device" "inverter" "${speicherpwip}" "${speicherpwuser}" "${speicherpwpass}" "1" >>"$MYLOGFILE" 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"
cat "${RAMDISKDIR}/pvwatt"
