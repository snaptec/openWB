#!/bin/bash
OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
#DMOD="EVU"
DMOD="MAIN"
Debug=$debug

#For development only
#Debug=1

if [ ${DMOD} == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/evu_json.log"
fi

openwbDebugLog ${DMOD} 2 "EVU KIT Version: ${evuflexversion}"
openwbDebugLog ${DMOD} 2 "EVU IP: ${evuflexip}"
openwbDebugLog ${DMOD} 2 "EVU Port : ${evuflexport}"
openwbDebugLog ${DMOD} 2 "EVU ID : ${evuflexid}"

#sudo python3 ${OPENWBBASEDIR}/modules/bezug_ethmpm3pm/test.py ${evuflexip} ${evuflexport} ${evuflexid} >>${MYLOGFILE} 2>&1
#ret=$?
if (( evuflexversion == 1 )); then
	python3 ${OPENWBBASEDIR}/modules/bezug_ethmpm3pm/readlovato.py ${evuflexip} ${evuflexport} ${evuflexid} >>${MYLOGFILE} 2>&1
	ret=$?
elif (( evuflexversion == 2 )); then
	python3 ${OPENWBBASEDIR}/modules/bezug_ethmpm3pm/readsdm.py ${evuflexip} ${evuflexport} ${evuflexid} >>${MYLOGFILE} 2>&1
	ret=$?
else
	python3 ${OPENWBBASEDIR}/modules/bezug_ethmpm3pm/readmpm3pm.py ${evuflexip} ${evuflexport} ${evuflexid} >>${MYLOGFILE} 2>&1
	ret=$?
fi
openwbDebugLog ${DMOD} 2 "EVU RET: ${ret}"

wattbezug=$(<${RAMDISKDIR}/wattbezug)
echo $wattbezug
