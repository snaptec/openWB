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
	MYLOGFILE="${RAMDISKDIR}/evu_janitza.log"
fi

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.janitza.device" "counter" "${bezug1_ip}" >>${MYLOGFILE} 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "EVU RET: ${ret}"

wattbezug=$(<${RAMDISKDIR}/wattbezug)
echo $wattbezug
