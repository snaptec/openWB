#!/bin/bash
OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
DMOD="PV"
#DMOD="MAIN"
Debug=$debug

#For development only
#Debug=1

if [ ${DMOD} == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/nurpv.log"
fi

#python3 ${OPENWBBASEDIR}/modules/wr_pvkitflex/test.py "2" ${pvflexip} ${pvflexport} ${pvflexid} >>${MYLOGFILE} 2>&1

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.openwb.device" "inverter" "${pvkitversion}" "2">>${MYLOGFILE} 2>&1

pvwatt=$(<${RAMDISKDIR}/pv2watt)
echo $pvwatt
