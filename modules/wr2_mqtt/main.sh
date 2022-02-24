#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
DMOD="PV"

pvwatt=$(<"${RAMDISKDIR}/pv2watt")
echo "$pvwatt"
openwbDebugLog ${DMOD} 1 "PV2Watt: ${pvwatt}"

pvkwh=$(<"${RAMDISKDIR}/pv2kwh")
openwbDebugLog ${DMOD} 1 "PV2kWh: ${pvkwh}"
openwbModulePublishState "$DMOD" 0 "Kein Fehler" 1
