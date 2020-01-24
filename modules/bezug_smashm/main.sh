#!/bin/bash

. /var/www/html/openWB/openwb.conf
if [[ "$smashmbezugid" != "none" ]]; then
	timeout 3 python3 /var/www/html/openWB/modules/bezug_smashm/sma-em-measurementwithserial.py $smashmbezugid
else
	timeout 3 python3 /var/www/html/openWB/modules/bezug_smashm/sma-em-measurement.py
fi
wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug
