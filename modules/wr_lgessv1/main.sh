#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
#MODULEDIR=$(cd `dirname $0` && pwd)
DMOD="PV"
#DMOD="MAIN"
Debug=$debug

#For Development only
#Debug=1

if [ $DMOD == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/nurpv.log"
fi

openwbDebugLog ${DMOD} 2 "WR IP: ${lgessv1ip}"
openwbDebugLog ${DMOD} 2 "WR Passwort: ${ess_pass}"
openwbDebugLog ${DMOD} 2 "WR Version: ${ess_api_ver}"

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.lg.device" "inverter" "${lgessv1ip}" "${ess_pass}"  "${ess_api_ver}" "1">>$MYLOGFILE 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

watt=$(<${RAMDISKDIR}/pvwatt)
echo ${watt}
