#!/bin/bash

OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
#DMOD="PV"
DMOD="MAIN"

if [ $DMOD == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/wr_solarwatt.log"
fi

openwbDebugLog ${DMOD} 2 "PV IP: ${speicher1_ip}"

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.solar_watt.device" "inverter" "${speicher1_ip}" >>"$MYLOGFILE" 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

cat "$RAMDISKDIR/pvwatt"
