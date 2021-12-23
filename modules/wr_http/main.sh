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
	MYLOGFILE="${RAMDISKDIR}/wr_http.log"
fi

openwbDebugLog ${DMOD} 2 "WR Leistung URL: ${wr_http_w_url}"
openwbDebugLog ${DMOD} 2 "WR Energie URL: ${wr_http_kwh_url}"

python3 /var/www/html/openWB/modules/wr_http/read_http.py "${wr_http_w_url}" "${wr_http_kwh_url}" >>$MYLOGFILE 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt) 
echo $pvwatt