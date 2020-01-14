#!/bin/bash

. /var/www/html/openWB/openwb.conf

timeout 3 python3 /var/www/html/openWB/modules/bezug_smashm/sma-em-measurement.py 
wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug
