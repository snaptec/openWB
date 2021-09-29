#!/bin/bash

python3 /var/www/html/openWB/packages/modules/counter/solax.py "${solaxip}"

wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug
