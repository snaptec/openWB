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
        MYLOGFILE="${RAMDISKDIR}/evu.log"
fi

timeout 3 bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.sma.device" "counter" "${smashmbezugid}" >>${MYLOGFILE} 2>&1
ret=$?
if [[ $ret -eq 124 ]] ; then
    openwbModulePublishState "EVU" 2 "Die Werte konnten nicht innerhalb des Timeouts abgefragt werden. Bitte Konfiguration und Gerätestatus prüfen."
    openwbDebugLog "MAIN" 0 "Fetching SMA counter data timed out"
else
    openwbDebugLog ${DMOD} 2 "EVU RET: ${ret}"
fi
wattbezug=$(<${RAMDISKDIR}/wattbezug)
echo $wattbezug
