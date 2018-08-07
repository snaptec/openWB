#!/bin/bash
. /var/www/html/openWB/openwb.conf
	if [[ $evsecons2 == "dac" ]]; then
		sudo python /var/www/html/openWB/runs/dac.py 0 $dacregisters2
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
		sudo python /var/www/html/openWB/runs/evsewritemodbus.py $evsesources2 $evseids2 0
	fi
	if [[ $evsecons2 == "simpleevsewifi" ]]; then
		output=$(curl --connect-timeout $evsewifitimeoutlp3 -s http://$evsewifiiplp3/getParameters)
		state=$(echo $output | jq '.list[] | .evseState')
		if ((state == true)) ; then
			curl --silent --connect-timeout $evsewifitimeoutlp3 -s http://$evsewifiiplp3/setStatus?active=false > /dev/null
		fi
	fi



echo 0 > /var/www/html/openWB/ramdisk/ladestatuss2
echo 0 > /var/www/html/openWB/ramdisk/llsolls2
