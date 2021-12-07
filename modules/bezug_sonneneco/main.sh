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
    MYLOGFILE="$RAMDISKDIR/bezug_sonneneco.log"
fi

openwbDebugLog ${DMOD} 2 "Bezug Sonneneco Alternativ: ${sonnenecoalternativ}"
openwbDebugLog ${DMOD} 2 "Bezug Sonneneco IP : ${sonnenecoip}"

python3 /var/www/html/openWB/modules/bezug_sonneneco/sonneneco.py "${sonnenecoalternativ}" "${sonnenecoip}" >>$MYLOGFILE 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug