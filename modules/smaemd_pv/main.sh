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




openwbDebugLog ${DMOD} 2 "SMA serials: ${smaemdpvid}"

timeout 3 bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.sma.device" "inverter" "${smaemdpvid}" "1">>$MYLOGFILE 2>&1
ret=$?

if [[ $ret -eq 124 ]] ; then
    openwbModulePublishState "PV" 2 "Die Werte konnten nicht innerhalb des Timeouts abgefragt werden. Bitte Konfiguration und Gerätestatus prüfen." "1"
    openwbDebugLog "MAIN" 0 "Fetching SMA counter data timed out"
else
    openwbDebugLog ${DMOD} 2 "EVU RET: ${ret}"
fi

watt=$(<${RAMDISKDIR}/pvwatt)
echo ${watt}
