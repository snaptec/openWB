#!/bin/bash

OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
DMOD="MAIN"


#For Development only
#Debug=1

if [ ${DMOD} == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/speicher.log"
fi


openwbDebugLog ${DMOD} 2 "Speicher IP: ${good_we_ip}"
openwbDebugLog ${DMOD} 2 "Speicher ID: ${good_we_id}"

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.good_we.device" "bat" "${good_we_ip}" "${good_we_id}" >>"$MYLOGFILE" 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

speicherleistung=$(<"${RAMDISKDIR}"/speicherleistung)

openwbDebugLog ${DMOD} 1 "BattLeistung: ${speicherleistung}"
