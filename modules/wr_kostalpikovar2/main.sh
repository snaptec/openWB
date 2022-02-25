#!/bin/bash

OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
#DMOD="EVU"
DMOD="MAIN"

if [ ${DMOD} == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/wr_kostalpikovar2.log"
fi

openwbDebugLog ${DMOD} 2 "WR User: ${wr_piko2_user}"
openwbDebugLog ${DMOD} 2 "WR Passwort: ${wr_piko2_pass}"
openwbDebugLog ${DMOD} 2 "WR URL: ${wr_piko2_url}"

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "wr_kostalpikovar2.kostal_piko_var2" 1 "${wr_piko2_url}" "${wr_piko2_user}" "${wr_piko2_pass}" >>"$MYLOGFILE" 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt) 
echo "$pvwatt"
