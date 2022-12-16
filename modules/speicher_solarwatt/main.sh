#!/bin/bash

OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
#DMOD="BATT"
DMOD="MAIN"

if [ ${DMOD} == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/speicher.log"
fi

openwbDebugLog ${DMOD} 2 "Speicher Methode: ${solarwattmethod}"
openwbDebugLog ${DMOD} 2 "Speicher IP1: ${speicher1_ip}"
openwbDebugLog ${DMOD} 2 "Speicher IP2: ${speicher1_ip2}"

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.solar_watt.device" "bat" "${speicher1_ip}" "${speicher1_ip2}" "${solarwattmethod}" >>"$MYLOGFILE" 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

speicherleistung=$(<"$RAMDISKDIR/speicherleistung")

openwbDebugLog ${DMOD} 1 "BattLeistung: ${speicherleistung}"
