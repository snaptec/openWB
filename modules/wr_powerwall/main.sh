#!/bin/bash

OPENWBBASEDIR=$(cd "$(dirname $0)/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
MODULEDIR=$(cd "$(dirname $0)" && pwd)
#DMOD="PV"
DMOD="MAIN"

if [ $DMOD == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/wr_powerwall.log"
fi

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "wr_powerwall.powerwall" "${speicherpwip}" "${speicherpwuser}" "${speicherpwpass}">>$MYLOGFILE 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"
pvwatt=$(<${RAMDISKDIR}/pvwatt) 
echo $pvwatt
