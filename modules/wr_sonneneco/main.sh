#!/bin/bash

OPENWBBASEDIR=$(cd "$(dirname $0)/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
#DMOD="PV"
DMOD="MAIN"

MYLOGFILE="${RAMDISKDIR}/openWB.log"

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.sonnenbatterie.device" "inverter" "${sonnenecoip}" "${sonnenecoalternativ}" "1" >>$MYLOGFILE 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

pvwatt=$(<${RAMDISKDIR}/pvwatt) 
echo $pvwatt
