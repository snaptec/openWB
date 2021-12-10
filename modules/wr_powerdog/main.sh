#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
#MODULEDIR=$(cd `dirname $0` && pwd)
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




openwbDebugLog ${DMOD} 2 "powerdog ip: ${bezug1_ip}"

python3 $OPENWBBASEDIR/packages/modules/powerdog/device.py "inverter" "${bezug1_ip}" "1">>$MYLOGFILE 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

watt=$(<${RAMDISKDIR}/pvwatt)
echo ${watt}
