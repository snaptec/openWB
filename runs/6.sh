#!/bin/bash
. /var/www/html/openWB/openwb.conf
if [[ $evsecon == "dac" ]]; then
		sudo python /var/www/html/openWB/runs/dac.py 790  $dacregister
fi
echo "setz ladung auf 6A" >> /var/www/html/openWB/web/lade.log
echo 1 > /var/www/html/openWB/ramdisk/ladestatus
echo 6 > /var/www/html/openWB/ramdisk/llsoll
