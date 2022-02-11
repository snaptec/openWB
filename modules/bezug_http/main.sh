#!/bin/bash
OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
#DMOD="EVU"
DMOD="MAIN"
Debug=$debug

#For development only
#Debug=1

if [ $DMOD == "MAIN" ]; then
    MYLOGFILE="$RAMDISKDIR/openWB.log"
else
    MYLOGFILE="$RAMDISKDIR/evu.log"
fi

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.http.device" "counter" "${bezug_http_w_url}" "${bezug_http_ikwh_url}" "${bezug_http_ekwh_url}" "${bezug_http_l1_url}" "${bezug_http_l2_url}" "${bezug_http_l3_url}" >>$MYLOGFILE 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug
