#!/bin/bash

python3 /var/www/html/openWB/modules/bezug_powerfox/powerfox.py "${powerfoxid}" "${powerfoxuser}" "${powerfoxpass}"
wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug
