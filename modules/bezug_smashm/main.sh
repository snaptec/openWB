#!/bin/bash

timeout 3 python3 /var/www/html/openWB/modules/bezug_smashm/sma-em-measurement.py $smashmbezugid
wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug
