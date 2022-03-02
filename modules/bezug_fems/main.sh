#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
#DMOD="EVU"
DMOD="MAIN"

if [ ${DMOD} == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/evu.log"
fi

openwbDebugLog ${DMOD} 2 "FEMS IP: ${femsip}"
openwbDebugLog ${DMOD} 2 "FEMS Passwort: ${femskacopw}"

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "bezug_fems.fems" "$femskacopw" "$femsip" >>"${MYLOGFILE}" 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "EVU RET: ${ret}"
cat "${RAMDISKDIR}/wattbezug"
