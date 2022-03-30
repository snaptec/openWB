#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
#DMOD="EVU"
DMOD="MAIN"
Debug=$debug

#For development only
#Debug=1

if [ ${DMOD} == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/wr_smartme.log"
fi

openwbDebugLog ${DMOD} 2 "WR URL: ${wr_smartme_url}"
openwbDebugLog ${DMOD} 2 "WR User: ${wr_smartme_user}"
openwbDebugLog ${DMOD} 2 "WR Passwort: ${wr_smartme_pass}"

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "wr_smartme.smartme" "${wr_smartme_url}" "${wr_smartme_user}" "${wr_smartme_pass}" >>$MYLOGFILE 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt) 
echo $pvwatt
