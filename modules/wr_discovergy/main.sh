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
	MYLOGFILE="${RAMDISKDIR}/wr_discovergy.log"
fi

openwbDebugLog ${DMOD} 2 "WR User: ${discovergyuser}"
openwbDebugLog ${DMOD} 2 "WR Passwort: ${discovergypass}"
openwbDebugLog ${DMOD} 2 "WR ID: ${discovergypvid}"

python3 /var/www/html/openWB/modules/wr_discovergy/discovergy.py "${discovergyuser}" "${discovergypass}" "${discovergypvid}" >>$MYLOGFILE 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt) 
echo $pvwatt
