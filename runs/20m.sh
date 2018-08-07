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
	if [[ $evsecon == "simpleevsewifi" ]]; then
		output=$(curl --connect-timeout $evsewifitimeoutlp1 -s http://$evsewifiiplp1/getParameters)
		state=$(echo $output | jq '.list[] | .evseState')
		if ((state == false)) ; then
			curl --silent --connect-timeout $evsewifitimeoutlp1 -s http://$evsewifiiplp1/setStatus?active=true > /dev/null
		fi
		current=$(echo $output | jq '.list[] | .actualCurrent')
		if (( current != 20 )) ; then
			curl --silent --connect-timeout $evsewifitimeoutlp1 -s http://$evsewifiiplp1/setCurrent?current=20 > /dev/null
		fi
	fi

echo 1 > /var/www/html/openWB/ramdisk/ladestatus
echo 20 > /var/www/html/openWB/ramdisk/llsoll
