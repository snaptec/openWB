#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname $0)/../../" && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd "$(dirname $0)" && pwd)
#DMOD="EVU"
DMOD="MAIN"

if [ $DMOD == "MAIN" ]; then
    MYLOGFILE="$RAMDISKDIR/openWB.log"
else
    MYLOGFILE="$RAMDISKDIR/bezug_sonneneco.log"
fi

python3 "${MODULEDIR}/sonneneco.py" "${sonnenecoip}" "${sonnenecoalternativ}" >>$MYLOGFILE 2>&1

wattbezug=$(<${RAMDISKDIR}/wattbezug)
echo $wattbezug
