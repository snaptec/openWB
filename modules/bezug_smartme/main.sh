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
    MYLOGFILE="$RAMDISKDIR/bezug_smartme.log"
fi

openwbDebugLog ${DMOD} 2 "Bezug Smartme URL: ${bezug_smartme_url}"
openwbDebugLog ${DMOD} 2 "Bezug Smartme User : ${bezug_smartme_user}"
openwbDebugLog ${DMOD} 2 "Bezug Smartme Passwort: ${bezug_smartme_pass}"

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "bezug_smartme.smartme" "${bezug_smartme_url}" "${bezug_smartme_user}" "${bezug_smartme_pass}" >>$MYLOGFILE 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug