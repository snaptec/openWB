#!/bin/bash

OPENWBBASEDIR=$(cd "$(dirname $0)/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
MODULEDIR=$(cd "$(dirname $0)" && pwd)
#DMOD="PV"
DMOD="MAIN"

MYLOGFILE="${RAMDISKDIR}/openWB.log"

python3 "${MODULEDIR}/sonneneco.py" "${sonnenecoip}" "${sonnenecoalternativ}" >>$MYLOGFILE 2>&1

pvwatt=$(<${RAMDISKDIR}/pvwatt) 
echo $pvwatt
