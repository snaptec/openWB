#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
#DMOD="EVU"
DMOD="MAIN"

if [ $DMOD == "MAIN" ]; then
	MYLOGFILE="$RAMDISKDIR/openWB.log"
else
	MYLOGFILE="$RAMDISKDIR/evu.log"
fi

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.http.device" "counter" "${bezug_http_w_url}" "${bezug_http_ikwh_url}" "${bezug_http_ekwh_url}" "${bezug_http_l1_url}" "${bezug_http_l2_url}" "${bezug_http_l3_url}" >>"$MYLOGFILE" 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

cat "${RAMDISKDIR}/wattbezug"
