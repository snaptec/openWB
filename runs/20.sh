#!/bin/bash
. /var/www/html/openWB/openwb.conf
if [[ $evsecon == "dac" ]]; then
	sudo python /var/www/html/openWB/runs/dac.py 2596 $dacregister
fi
if [[ $evsecon == "modbusevse" ]]; then
	sudo python /var/www/html/openWB/runs/evsewritemodbus.py $modbusevsesource $modbusevseid 20
fi
if [[ $debug == "2" ]]; then
	echo "setz ladung auf 20A" >> /var/www/html/openWB/web/lade.log
fi
echo 1 > /var/www/html/openWB/ramdisk/ladestatus
echo 20 > /var/www/html/openWB/ramdisk/llsoll
