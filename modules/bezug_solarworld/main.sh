#!/bin/bash

python3 /var/www/html/openWB/modules/bezug_solarworld/solarworld.py "${solarworld_emanagerip}"
wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug