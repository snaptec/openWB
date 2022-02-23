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

#
# Exportere Volt/Ampere/Frequenz etc in die Ramdisk
#   
bash "$OPENWBBASEDIR/packages/legacy_run.sh" "bezug_rct2.rct_read_bezug" "${bezug1_ip}" >>${MYLOGFILE} 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

#
# Nehme wattbezug als ergbenis mit zurueck da beim Bezug-Module ein Returnwert erwartet wird.
#  
wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug
