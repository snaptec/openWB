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

openwbDebugLog ${DMOD} 2 "WR IP: ${wrfroniusip}"
openwbDebugLog ${DMOD} 2 "WR IP2: ${wrfronius2ip}"
openwbDebugLog ${DMOD} 2 "WR Speicher: ${speichermodul}"

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.fronius.device" "inverter" "${wrfroniusip}" "0" "0" "${wrfronius2ip}" "1" >>"$MYLOGFILE" 2>&1

cat "${RAMDISKDIR}/pvwatt"
