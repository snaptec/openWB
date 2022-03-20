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
bash "$OPENWBBASEDIR/packages/legacy_run.sh" "wr2_ethsdm120.readsdm120" "${pv2ip}" "${pv2id}" "${pv2ip2}" "${pv2id2}" >>${MYLOGFILE} 2>&1 
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"
pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)
echo $pvwatt
