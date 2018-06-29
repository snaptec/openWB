#!/bin/bash
. /var/www/html/openWB/openwb.conf

	if [[ $evsecons1 == "dac" ]]; then
		sudo python /var/www/html/openWB/runs/dac.py 2596 $dacregisters1
	fi

	if [[ $evsecons1 == "modbusevse" ]]; then
		sudo python /var/www/html/openWB/runs/evsewritemodbus.py $evsesources1 $evseids1 20
	fi

echo 1 > /var/www/html/openWB/ramdisk/ladestatuss1
echo 20 > /var/www/html/openWB/ramdisk/llsolls1
