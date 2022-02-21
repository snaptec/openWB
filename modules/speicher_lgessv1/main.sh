#!/bin/bash

OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
MODULEDIR=$(cd "$(dirname "$0")" && pwd)
#DMOD="BATT"
DMOD="MAIN"

if [ ${DMOD} == "MAIN" ]; then
    MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
    MYLOGFILE="${RAMDISKDIR}/speicher.log"
fi

openwbDebugLog ${DMOD} 2 "Speicher IP: ${lgessv1ip}"
openwbDebugLog ${DMOD} 2 "Speicher Passwort: ${lgessv1pass}"
openwbDebugLog ${DMOD} 2 "Speicher Version: ${ess_api_ver}"

python3 "$MODULEDIR/lgessv1.py" "${lgessv1ip}" "${lgessv1pass}" "${ess_api_ver}" >>"$MYLOGFILE" 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

speicherleistung=$(<"${RAMDISKDIR}/speicherleistung")

openwbDebugLog ${DMOD} 1 "BattLeistung: ${speicherleistung}"