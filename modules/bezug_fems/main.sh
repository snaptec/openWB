#!/bin/bash

sudo python3 /var/www/html/openWB/modules/bezug_fems/fems.py $femskacopw $femsip
wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug
