#!/bin/bash

OPENWBBASEDIR=$(cd "$(dirname $0)/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
#DMOD="PV"
DMOD="MAIN"

MYLOGFILE="${RAMDISKDIR}/openWB.log"

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.sma_modbus_tcp.device" "${tri9000ip}" "${wrsmawebbox}" "${wrsma2ip}" "${wrsma3ip}" "${wrsma4ip}" "1" >>$MYLOGFILE 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

pvwatt=$(<${RAMDISKDIR}/pvwatt) 
echo $pvwatt