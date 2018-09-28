#!/bin/bash
. /var/www/html/openWB/openwb.conf
	if [[ $evsecons1 == "dac" ]]; then
		sudo python /var/www/html/openWB/runs/dac.py 0 $dacregisters1
	fi

	if [[ $evsecons1 == "modbusevse" ]]; then
		if [[ $evsesources1 = *virtual* ]]
		then
			if pgrep -f "socat pty,link=$evsesources1,raw tcp:$evselanips1:26" > /dev/null
			then
				echo "test" > /dev/null
			else
				sudo socat pty,link=$evsesources1,raw tcp:$evselanips1:26 &
			fi
		else
			echo "echo" > /dev/null
		fi	
		sudo python /var/www/html/openWB/runs/evsewritemodbus.py $evsesources1 $evseids1 0
	fi
	if [[ $evsecons1 == "simpleevsewifi" ]]; then
		output=$(curl --connect-timeout $evsewifitimeoutlp2 -s http://$evsewifiiplp2/getParameters)
		state=$(echo $output | jq '.list[] | .evseState')
		if ((state == true)) ; then
			curl --silent --connect-timeout $evsewifitimeoutlp2 -s http://$evsewifiiplp2/setStatus?active=false > /dev/null
		fi
	fi
echo 0 > /var/www/html/openWB/ramdisk/ladestatuss1
echo 0 > /var/www/html/openWB/ramdisk/llsolls1
