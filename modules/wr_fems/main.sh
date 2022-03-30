#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
#DMOD="EVU"
DMOD="MAIN"

if [ ${DMOD} == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/wr_fems.log"
fi

openwbDebugLog ${DMOD} 2 "WR Passwort: ${femskacopw}"
openwbDebugLog ${DMOD} 2 "WR IP: ${femsip}"

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "wr_fems.fems" "${femskacopw}" "${femsip}" >>"${MYLOGFILE}" 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"
pvwatt=$(<"$RAMDISKDIR/pvwatt") 
echo "$pvwatt"
