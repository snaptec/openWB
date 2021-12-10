#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
#MODULEDIR=$(cd `dirname $0` && pwd)
#DMOD="PV"
DMOD="MAIN"
Debug=$debug

#For Development only
#Debug=1

if [ $DMOD == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/wr_powerwall.log"
fi

openwbDebugLog ${DMOD} 2 "PV Login erforderlich: ${speicherpwloginneeded}"
openwbDebugLog ${DMOD} 2 "PV User: ${speicherpwuser}"
openwbDebugLog ${DMOD} 2 "PV Passwort: ${speicherpwpass}"
openwbDebugLog ${DMOD} 2 "PV IP: ${speicherpwip}"

python3 /var/www/html/openWB/modules/wr_powerwall/powerwall.py "${OPENWBBASEDIR}" "${speicherpwloginneeded}" "${speicherpwuser}" "${speicherpwpass}" "${speicherpwip}" >>$MYLOGFILE 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt) 
echo $pvwatt