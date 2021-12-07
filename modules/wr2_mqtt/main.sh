#!/bin/bash
OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
DMOD="PV"
Debug=$debug


pvwatt=$(<${RAMDISKDIR}/pv2watt)
echo $pvwatt
openwbDebugLog ${DMOD} 1 "PV2Watt: ${pvwatt}"

pvkwh=$(<${RAMDISKDIR}/pv2kwh)
openwbDebugLog ${DMOD} 1 "PV2kWh: ${pvkwh}"
openwbModulePublishState "PV" 0 "Kein Fehler" 1
