#!/bin/bash
. /var/www/html/openWB/openwb.conf
	if [[ $evsecons2 == "dac" ]]; then
		sudo python /var/www/html/openWB/runs/dac.py 1038 $dacregisters2
	fi

	if [[ $evsecons2 == "modbusevse" ]]; then
		if [[ $evsesources2 = *virtual* ]]
		then
			if ps ax |grep -v grep |grep "socat pty,link=$evsesources2,raw tcp:$evselanips2:26" > /dev/null
			then
				echo "test" > /dev/null
			else
				sudo socat pty,link=$evsesources2,raw tcp:$evselanips2:26 &
			fi
		else
			echo "echo" > /dev/null
		fi	
		sudo python /var/www/html/openWB/runs/evsewritemodbus.py $evsesources2 $evseids2 8
	fi
echo 8 > /var/www/html/openWB/ramdisk/llsolls2
echo 1 > /var/www/html/openWB/ramdisk/ladestatuss2
