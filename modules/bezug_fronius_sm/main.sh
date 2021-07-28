#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
DMOD="MAIN"

# check if config file is already in env
if [[ -z "$debug" ]]; then
	echo "bezug_fronius_sm: Seems like openwb.conf is not loaded. Reading file."
	# try to load config
	. $OPENWBBASEDIR/loadconfig.sh
	# load helperFunctions
	. $OPENWBBASEDIR/helperFunctions.sh
fi

ret=$(python3 /var/www/html/openWB/modules/bezug_fronius_sm/fronius_sm.py) 2>&1 > /dev/null)

response_sm=$(echo $ret | awk '{print $1}' | tr -d '[' | tr -d ',')
meter_location=$(echo $ret | awk '{print $2}' | tr -d ',')
response_fi=$(echo $ret | awk '{print $3}' | tr -d ']')
wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
evuv1=$(</var/www/html/openWB/ramdisk/evuv1)
evuv2=$(</var/www/html/openWB/ramdisk/evuv2)
evuv3=$(</var/www/html/openWB/ramdisk/evuv3)
bezugw1=$(</var/www/html/openWB/ramdisk/bezugw1)
bezugw2=$(</var/www/html/openWB/ramdisk/bezugw2)
bezugw3=$(</var/www/html/openWB/ramdisk/bezugw3)
bezuga1=$(</var/www/html/openWB/ramdisk/bezuga1)
bezuga2=$(</var/www/html/openWB/ramdisk/bezuga2)
bezuga3=$(</var/www/html/openWB/ramdisk/bezuga3)
echo $wattbezug

openwbDebugLog ${DMOD} 2 "EVU: response_sm: $response_sm"
openwbDebugLog ${DMOD} 1 "EVU: SmartMeter location: $"
openwbDebugLog ${DMOD} 1 "EVU: V: ${evuv1}/${evuv2}/${evuv3} A: ${bezuga1}/${bezuga2}/${bezuga3} W: ${bezugw1}/${bezugw2}/${bezugw3}/T${wattbezug}"



