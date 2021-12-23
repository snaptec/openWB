#!/bin/bash
OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
DMOD="PV"
Debug=$debug

pvwatt=$(<${RAMDISKDIR}/pvwatt)
echo $pvwatt
openwbDebugLog ${DMOD} 1 "PVWatt: ${pvwatt}"

pvkwh=$(<${RAMDISKDIR}/pvkwh)
openwbDebugLog ${DMOD} 1 "PVkWh: ${pvkwh}"

openwbModulePublishState "PV" 0 "Kein Fehler" 1
