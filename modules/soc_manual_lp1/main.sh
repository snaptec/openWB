#!/bin/sh

soc=$(cat /var/www/html/openWB/ramdisk/lp1_manual_soc)
soc=$(echo $soc |sed 's/\..*$//')
echo $soc > /var/www/html/openWB/ramdisk/soc
