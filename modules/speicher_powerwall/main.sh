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

openwbDebugLog ${DMOD} 2 "Speicher Login erforderlich: ${speicherpwloginneeded}"
openwbDebugLog ${DMOD} 2 "Speicher User: ${speicherpwuser}"
openwbDebugLog ${DMOD} 2 "Speicher Passwort: ${speicherpwpass}"
openwbDebugLog ${DMOD} 2 "Speicher IP: ${speicherpwip}"

python3 /var/www/html/openWB/modules/speicher_powerwall/powerwall.py "${speicherpwip}" "${speicherpwuser}" "${speicherpwpass}" >>$MYLOGFILE 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

speicherleistung=$(<${RAMDISKDIR}/speicherleistung)

openwbDebugLog ${DMOD} 1 "BattLeistung: ${speicherleistung}"
