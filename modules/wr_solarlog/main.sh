#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname $0)/../../" && pwd)
MODULEDIR=$(cd "$(dirname $0)" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
MYLOGFILE="${RAMDISKDIR}/nurpv.log"

DMOD="PV"
Debug=$debug

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.solar_log.device" "inverter" "${bezug_solarlog_ip}" "0">> "${MYLOGFILE}" 2>&1
ret=$?
openwbDebugLog ${DMOD} 2 "RET: ${ret}"

cat "$RAMDISKDIR/pvwatt"
