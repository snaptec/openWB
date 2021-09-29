#!/bin/bash

python3 /var/www/html/openWB/packages/modules/counter/fems.py "${femskacopw}" "${femsip}"

wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug
