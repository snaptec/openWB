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

openwbDebugLog ${DMOD} 2 "EVU URL: ${bezugjsonurl}"
openwbDebugLog ${DMOD} 2 "Filter Watt : ${bezugjsonwatt}"
openwbDebugLog ${DMOD} 2 "Filter Bezug: ${bezugjsonkwh}"
openwbDebugLog ${DMOD} 2 "Filter Einsp: ${einspeisungjsonkwh}"

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.json.device" "counter" "${bezugjsonurl}" "${bezugjsonwatt}" "${bezugjsonkwh}" "${einspeisungjsonkwh}" >>$MYLOGFILE 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

evuwatt=$(<${RAMDISKDIR}/wattbezug)
echo ${evuwatt}
