#!/bin/bash
OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
#DMOD="BAT"
DMOD="MAIN"
Debug=$debug

#For development only
#Debug=1

if [ ${DMOD} == "MAIN" ]; then
        MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
        MYLOGFILE="${RAMDISKDIR}/bat.log"
fi

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.solax.device" "bat" "${solaxip}" >>${MYLOGFILE} 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "BAT RET: ${ret}"
