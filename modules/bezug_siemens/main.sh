#!/bin/bash

sudo python3 /var/www/html/openWB/packages/modules/counter/siemens.py "${bezug1_ip}"

wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug
