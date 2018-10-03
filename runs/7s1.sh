#!/bin/bash
. /var/www/html/openWB/openwb.conf
if [[ $evsecons1 == "dac" ]]; then
		sudo python /var/www/html/openWB/runs/dac.py 908 $dacregisters1
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
		sudo python /var/www/html/openWB/runs/evsewritemodbus.py $evsesources1 $evseids1 7
	fi
	if [[ $evsecons1 == "simpleevsewifi" ]]; then
		output=$(curl --connect-timeout $evsewifitimeoutlp2 -s http://$evsewifiiplp2/getParameters)
		state=$(echo $output | jq '.list[] | .evseState')
		if ((state == false)) ; then
			curl --silent --connect-timeout $evsewifitimeoutlp2 -s http://$evsewifiiplp2/setStatus?active=true > /dev/null
		fi
		current=$(echo $output | jq '.list[] | .actualCurrent')
		if (( current != 7 )) ; then
			curl --silent --connect-timeout $evsewifitimeoutlp2 -s http://$evsewifiiplp2/setCurrent?current=7 > /dev/null
		fi
	fi
echo 1 > /var/www/html/openWB/ramdisk/ladestatuss1
echo 7 > /var/www/html/openWB/ramdisk/llsolls1
