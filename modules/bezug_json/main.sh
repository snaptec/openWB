#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
#DMOD="EVU"
DMOD="MAIN"
Debug=$debug

python3 /var/www/html/openWB/modules/bezug_json/read_json.py "${bezugjsonurl}" "${bezugjsonwatt}" "${bezugjsonkwh}" "${einspeisungjsonkwh}"

#For development only
#Debug=1

openwbDebugLog ${DMOD} 2 "${bezugjsonwatt}"
openwbDebugLog ${DMOD} 2 "${bezugjsonkwh}"
openwbDebugLog ${DMOD} 2 "${einspeisungjsonkwh}"

evuwatt=$(</var/www/html/openWB/ramdisk/wattbezug)
echo ${evuwatt}
openwbDebugLog  ${DMOD} 1 "Watt: ${evuwatt}"
evuikwh=$(</var/www/html/openWB/ramdisk/bezugkwh)
openwbDebugLog ${DMOD} 1 "BezugkWh: ${evuikwh}"
evuekwh=$(</var/www/html/openWB/ramdisk/einspeisungkwh)
openwbDebugLog ${DMOD} 1 "EinspeiskWh: ${evuekwh}"

