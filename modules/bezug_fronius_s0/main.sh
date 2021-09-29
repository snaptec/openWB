#!/bin/bash

python3 /var/www/html/openWB/packages/modules/counter/fronius_s0.py "${froniusprimo}" "${wrfroniusip}"

wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug
