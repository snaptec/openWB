#!/bin/bash
. /var/www/html/openWB/openwb.conf
if [[ $evsecon == "dac" ]]; then
		sudo python /var/www/html/openWB/runs/dac.py 1557 $dacregister
fi
if [[ $evsecon == "modbusevse" ]]; then
	sudo python /var/www/html/openWB/runs/evsewritemodbus.py $modbusevsesource $modbusevseid 12
fi
if [[ $debug == "2" ]]; then
	echo "setz ladung auf 12A" >> /var/www/html/openWB/web/lade.log
fi
echo 12 > /var/www/html/openWB/ramdisk/llsoll
echo 1 > /var/www/html/openWB/ramdisk/ladestatus
