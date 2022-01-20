#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname $0)/../../" && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
#DMOD="EVU"
DMOD="MAIN"

if [ $DMOD == "MAIN" ]; then
    MYLOGFILE="$RAMDISKDIR/openWB.log"
else
    MYLOGFILE="$RAMDISKDIR/bezug_sonneneco.log"
fi

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.sonnenbatterie.device" "counter" "${sonnenecoip}" "${sonnenecoalternativ}" >>$MYLOGFILE 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

wattbezug=$(<${RAMDISKDIR}/wattbezug)
echo $wattbezug
