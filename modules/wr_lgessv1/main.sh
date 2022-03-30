#!/bin/bash

OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
MODULEDIR=$(cd "$(dirname "$0")" && pwd)
#DMOD="EVU"
DMOD="MAIN"

if [ ${DMOD} == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/wr_lgessv1.log"
fi

openwbDebugLog ${DMOD} 2 "WR IP: ${lgessv1ip}"
openwbDebugLog ${DMOD} 2 "WR Passwort: ${ess_pass}"
openwbDebugLog ${DMOD} 2 "WR Version: ${ess_api_ver}"

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "wr_lgessv1.lgessv1" "${lgessv1ip}" "${ess_pass}" "${ess_api_ver}" >>$MYLOGFILE 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt) 
echo "$pvwatt"
