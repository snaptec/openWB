#!/bin/bash

sudo python3 /var/www/html/openWB/packages/modules/pv/powerdog.py "${bezug1_ip}"

wattbezug=$(</var/www/html/openWB/ramdisk/pvwatt)
echo $wattbezug
