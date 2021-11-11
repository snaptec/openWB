#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
#MODULEDIR=$(cd `dirname $0` && pwd)
#DMOD="BATT"
DMOD="MAIN"
Debug=$debug

#For Development only
#Debug=1

if [ ${DMOD} == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/speicher.log"
fi


openwbDebugLog ${DMOD} 2 "Speicher URL: ${battjsonurl}"
openwbDebugLog ${DMOD} 2 "Speicher Watt: ${battjsonwatt}"
openwbDebugLog ${DMOD} 2 "Speicher SoC: ${battjsonsoc}"

python3 $OPENWBBASEDIR/modules/speicher_json/read_json.py "${battjsonurl}" "${battjsonwatt}" "${battjsonsoc}" >>$MYLOGFILE 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

speicherleistung=$(<${RAMDISKDIR}/speicherleistung)

openwbDebugLog ${DMOD} 1 "BattLeistung: ${speicherleistung}"
#echo ${speicherleistung}
