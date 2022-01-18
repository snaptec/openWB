#!/bin/bash

OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
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

inverter_num=${1:-1}
[[ "$inverter_num" -gt 1 ]] && config_prefix="wr$1" || config_prefix="wr"
declare -n "config_url=${config_prefix}jsonurl"
declare -n "config_watt=${config_prefix}jsonwatt"
declare -n "config_kwh=${config_prefix}jsonkwh"

openwbDebugLog ${DMOD} 2 "PV URL : ${config_url}"
openwbDebugLog ${DMOD} 2 "PV Watt: ${config_watt}"
openwbDebugLog ${DMOD} 2 "PV kWh : ${config_kwh}"

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.json.device" "inverter" "$config_url" "$config_watt" "$config_kwh" "$inverter_num" >>"$MYLOGFILE" 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

cat "${RAMDISKDIR}/pvwatt"
