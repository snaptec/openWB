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

python3 "${MODULEDIR}/powerwall.py" "${speicherpwip}" "${speicherpwuser}" "${speicherpwpass}" >>$MYLOGFILE 2>&1

pvwatt=$(<${RAMDISKDIR}/pvwatt) 
echo $pvwatt
