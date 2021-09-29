#!/bin/bash

python3 /var/www/html/openWB/packages/modules/counter/varta.py "${vartaspeicherip}"

wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug
