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

if (( pv2kitversion == 0 )); then
	python3 ${OPENWBBASEDIR}/modules/wr_pvkit/readlovato.py "2" "192.168.193.13" "8899" "8" >>${MYLOGFILE} 2>&1
elif (( pv2kitversion == 1 )); then
	python3 ${OPENWBBASEDIR}/modules/wr_pvkit/readsdm.py "2" "192.168.193.13" "8899" "116" >>${MYLOGFILE} 2>&1
else
	echo "bla" > /dev/null
	#python3 ${OPENWBBASEDIR}/modules/wr_pvkit/readmpm3pm.py "2" "192.168.193.13" "8899" "8" >>${MYLOGFILE} 2>&1
fi
pvwatt=$(<${RAMDISKDIR}/pv2watt)
echo $pvwatt
