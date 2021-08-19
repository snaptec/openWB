#!/bin/bash

python3 /var/www/html/openWB/modules/bezug_smartfox/smartfox.py "${bezug_smartfox_ip}"
wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug