#!/bin/bash

sudo python3 /var/www/html/openWB/packages/modules/counter/sbs25.py "${sbs25ip}"

wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug
