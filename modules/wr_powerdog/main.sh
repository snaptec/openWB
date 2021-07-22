#!/bin/bash

sudo python /var/www/html/openWB/modules/wr_powerdog/powerdog.py $bezug1_ip
wattbezug=$(</var/www/html/openWB/ramdisk/pvwatt)
echo $wattbezug
