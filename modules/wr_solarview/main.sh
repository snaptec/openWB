#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
#MODULEDIR=$(cd `dirname $0` && pwd)
#DMOD="PV"
DMOD="MAIN"
Debug=$debug

#For Development only
#Debug=1

if [ $DMOD == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/wr_solarview.log"
fi

openwbDebugLog ${DMOD} 2 "PV Hostname: ${solarview_hostname}"
openwbDebugLog ${DMOD} 2 "PV Port: ${solarview_port}"
openwbDebugLog ${DMOD} 2 "PV Timeout: ${solarview_timeout}"
openwbDebugLog ${DMOD} 2 "PV Command: ${solarview_command_wr}"


bash "$OPENWBBASEDIR/packages/legacy_run.sh" "wr_solarview.solarview" "${solarview_hostname}" "${solarview_port}" "${solarview_timeout}" "${solarview_command_wr}" >>$MYLOGFILE 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt) 
echo $pvwatt