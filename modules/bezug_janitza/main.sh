#!/bin/bash

python3 /var/www/html/openWB/packages/modules/counter/janitza.py "${bezug1_ip}"

wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug
