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


bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.studer.device" "inverter" "${studer_ip}" "${studer_vc}" "${studer_vc_type}" "1">>${MYLOGFILE} 2>&1

pvwatt=$(<${RAMDISKDIR}/pvwatt)
echo $pvwatt
