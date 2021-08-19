#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
Debug=$debug

python3 /var/www/html/openWB/modules/bezug_solarwatt/solarwatt.py "${OPENWBBASEDIR}" "${Debug}" "${solarwattmethod}" "${speicher1_ip}" "${speicher1_ip2}"
wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug