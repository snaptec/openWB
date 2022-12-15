#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
#DMOD="EVU"
DMOD="MAIN"

if [ $DMOD == "MAIN" ]; then
	MYLOGFILE="$RAMDISKDIR/openWB.log"
else
	MYLOGFILE="$RAMDISKDIR/bezug_smartme.log"
fi

openwbDebugLog ${DMOD} 2 "Bezug Smartme URL: ${bezug_smartme_url}"
openwbDebugLog ${DMOD} 2 "Bezug Smartme User : ${bezug_smartme_user}"
openwbDebugLog ${DMOD} 2 "Bezug Smartme Passwort: ${bezug_smartme_pass}"

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.smart_me.device" "counter" "${bezug_smartme_user}" "${bezug_smartme_pass}" "${bezug_smartme_url}" >>"$MYLOGFILE" 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

cat "${RAMDISKDIR}/wattbezug"
