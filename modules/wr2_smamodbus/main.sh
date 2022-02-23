#!/bin/bash

OPENWBBASEDIR=$(cd "$(dirname $0)/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
#DMOD="PV"
DMOD="MAIN"

MYLOGFILE="${RAMDISKDIR}/openWB.log"

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.sma_modbus_tcp.device" "${pv2ip}" "0" "none" "none" "none" "2" >>"$MYLOGFILE" 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

pv2watt=$(</var/www/html/openWB/ramdisk/pv2watt)
echo $pv2watt
