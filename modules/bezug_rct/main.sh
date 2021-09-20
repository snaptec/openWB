#!/bin/bash

sudo python3 /var/www/html/openWB/packages/modules/counter/rct.py "${bezug1_ip}"

wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug

