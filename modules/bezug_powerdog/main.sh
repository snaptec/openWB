#!/bin/bash

sudo python /var/www/html/openWB/modules/bezug_powerdog/powerdog.py $bezug1_ip
wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug
