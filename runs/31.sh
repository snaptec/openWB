#!/bin/bash
. /var/www/html/openWB/openwb.conf
if [[ $evsecon == "dac" ]]; then
	sudo python /var/www/html/openWB/runs/dac.py 4024 $dacregister
fi
if [[ $evsecon == "modbusevse" ]]; then
	sudo python /var/www/html/openWB/runs/evsewritemodbus.py $modbusevsesource $modbusevseid 31
fi
if [[ $debug == "2" ]]; then
	echo "setz ladung auf 31A" >> /var/www/html/openWB/web/lade.log
fi
if [[ $lastmanagement == "1" ]]; then
	if [[ $evsecons1 == "dac" ]]; then
		sudo python /var/www/html/openWB/runs/dac.py 4024 $dacregisters1
	fi

	if [[ $evsecons1 == "modbusevse" ]]; then
		sudo python /var/www/html/openWB/runs/evsewritemodbus.py $evsesources1 $evseids1 31
	fi
	echo 31 > /var/www/html/openWB/ramdisk/llsolls1
	echo 1 > /var/www/html/openWB/ramdisk/ladestatuss1
fi
if [[ $lastmanagements2 == "1" ]]; then
	if [[ $evsecons2 == "dac" ]]; then
		sudo python /var/www/html/openWB/runs/dac.py 4024 $dacregisters2
	fi
	if [[ $evsecons2 == "modbusevse" ]]; then
		sudo python /var/www/html/openWB/runs/evsewritemodbus.py $evsesources2 $evseids2 31
	fi
	echo 31 > /var/www/html/openWB/ramdisk/ladestatuss2
	echo 1 > /var/www/html/openWB/ramdisk/llsolls2
fi
echo 31 > /var/www/html/openWB/ramdisk/llsoll
echo 1 > /var/www/html/openWB/ramdisk/ladestatus
