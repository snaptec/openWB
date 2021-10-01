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
        MYLOGFILE="${RAMDISKDIR}/evu.log"
fi

openwbDebugLog ${DMOD} 2 "EVU Kit Version: ${evukitversion}"

if (( evukitversion == 1 )); then
	sudo python ${OPENWBBASEDIR}/modules/bezug_ethmpm3pm/readlovato.py >>${MYLOGFILE} 2>&1
	ret=$?
elif (( evukitversion == 2 )); then
	sudo python ${OPENWBBASEDIR}/modules/bezug_ethmpm3pm/readsdm.py >>${MYLOGFILE} 2>&1
	ret=$?
else
	sudo python ${OPENWBBASEDIR}/modules/bezug_ethmpm3pm/readmpm3pm.py >>${MYLOGFILE} 2>&1
	ret=$?
fi

openwbDebugLog ${DMOD} 2 "EVU RET: ${ret}"
wattbezug=$(<${RAMDISKDIR}/wattbezug)
echo $wattbezug
