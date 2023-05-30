#!/bin/bash

OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
#MODULEDIR=$(cd `dirname $0` && pwd)
#DMOD="PV"
DMOD="MAIN"
Debug=$debug

#For Development only
#Debug=1

if [ $DMOD == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/wr_solarworld.log"
fi

openwbDebugLog ${DMOD} 2 "PV IP: ${solarworld_emanagerip}"

bash "$OPENWBBASEDIR/packages/legacy_run.sh"  "modules.devices.solar_world.device" "inverter" "${solarworld_emanagerip}" "1" >>"$MYLOGFILE" 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"
cat "${RAMDISKDIR}/pvwatt"
