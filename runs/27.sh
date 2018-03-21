#!/bin/bash
. /var/www/html/openWB/openwb.conf
if [[ $evsecon == "dac" ]]; then
	sudo python /var/www/html/openWB/runs/dac.py 3505 $dacregister
fi
if [[ $debug == "2" ]]; then
	echo "setz ladung auf 27A" >> /var/www/html/openWB/web/lade.log
fi
echo 27 > /var/www/html/openWB/ramdisk/llsoll
echo 1 > /var/www/html/openWB/ramdisk/ladestatus
