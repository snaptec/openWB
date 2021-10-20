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

openwbDebugLog ${DMOD} 2 "PV KIT Version: ${pv2flexversion}"
openwbDebugLog ${DMOD} 2 "PV IP: ${pv2flexip}"
openwbDebugLog ${DMOD} 2 "PV Port : ${pv2flexport}"
openwbDebugLog ${DMOD} 2 "PV ID : ${pv2flexid}"



#python3 ${OPENWBBASEDIR}/modules/wr_pvkitflex/test.py "2" ${pv2flexip} ${pv2flexport} ${pv2flexid} >>${MYLOGFILE} 2>&1

if (( pv2flexversion == 1 )); then
	python3 ${OPENWBBASEDIR}/modules/wr_pvkit/readlovato.py "2" ${pv2flexip} ${pv2flexport} ${pv2flexid} >>${MYLOGFILE} 2>&1
elif (( pv2flexversion == 2 )); then
	python3 ${OPENWBBASEDIR}/modules/wr_pvkit/readsdm.py "2" ${pv2flexip} ${pv2flexport} ${pv2flexid} >>${MYLOGFILE} 2>&1
else
	python3 ${OPENWBBASEDIR}/modules/wr_pvkit/readmpm3pm.py "2" ${pv2flexip} ${pv2flexport} ${pv2flexid} >>${MYLOGFILE} 2>&1
fi
pvwatt=$(<${RAMDISKDIR}/pv2watt)
echo $pvwatt
