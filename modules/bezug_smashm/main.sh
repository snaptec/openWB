#!/bin/bash

python3 /var/www/html/openWB/packages/modules/counter/sma.py "${smashmbezugid}"

wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug
