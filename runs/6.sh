#!/bin/bash
. /var/www/html/openWB/openwb.conf
if [[ $evsecon == "dac" ]]; then
	sudo python /var/www/html/openWB/runs/dac.py 790 $dacregister
fi
if [[ $evsecon == "modbusevse" ]]; then
	if [[ $modbusevsesource = *virtual* ]]
	then
		if pgrep -f "socat pty,link=$modbusevsesource,raw tcp:$modbusevselanip:26" > /dev/null
		then
			echo "test" > /dev/null
		else
			sudo socat pty,link=$modbusevsesource,raw tcp:$modbusevselanip:26 &
		fi
	else
		echo "echo" > /dev/null
	fi				
	sudo python /var/www/html/openWB/runs/evsewritemodbus.py $modbusevsesource $modbusevseid 6
fi
	if [[ $evsecon == "simpleevsewifi" ]]; then
		output=$(curl --connect-timeout $evsewifitimeoutlp1 -s http://$evsewifiiplp1/getParameters)
		state=$(echo $output | jq '.list[] | .evseState')
		if ((state == false)) ; then
			curl --silent --connect-timeout $evsewifitimeoutlp1 -s http://$evsewifiiplp1/setStatus?active=true > /dev/null
		fi
		current=$(echo $output | jq '.list[] | .actualCurrent')
		if (( current != 6 )) ; then
			curl --silent --connect-timeout $evsewifitimeoutlp1 -s http://$evsewifiiplp1/setCurrent?current=6 > /dev/null
		fi
	fi

if [[ $debug == "2" ]]; then
	echo "setz ladung auf 6A" >> /var/www/html/openWB/web/lade.log
fi
if [[ $lastmanagement == "1" ]]; then
	if [[ $evsecons1 == "dac" ]]; then
		sudo python /var/www/html/openWB/runs/dac.py 790 $dacregisters1
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

		sudo python /var/www/html/openWB/runs/evsewritemodbus.py $evsesources1 $evseids1 6
	fi
	if [[ $evsecons1 == "simpleevsewifi" ]]; then
		output=$(curl --connect-timeout $evsewifitimeoutlp2 -s http://$evsewifiiplp2/getParameters)
		state=$(echo $output | jq '.list[] | .evseState')
		if ((state == false)) ; then
			curl --silent --connect-timeout $evsewifitimeoutlp2 -s http://$evsewifiiplp2/setStatus?active=true > /dev/null
		fi
		current=$(echo $output | jq '.list[] | .actualCurrent')
		if (( current != 6 )) ; then
			curl --silent --connect-timeout $evsewifitimeoutlp2 -s http://$evsewifiiplp2/setCurrent?current=6 > /dev/null
		fi
	fi

	echo 1 > /var/www/html/openWB/ramdisk/ladestatuss1
	echo 6 > /var/www/html/openWB/ramdisk/llsolls1

fi
if [[ $lastmanagements2 == "1" ]]; then
		if [[ $evsecons2 == "dac" ]]; then
			sudo python /var/www/html/openWB/runs/dac.py 790 $dacregisters2
		fi
		if [[ $evsecons2 == "modbusevse" ]]; then
			if [[ $evsesources2 = *virtual* ]]
			then
				if pgrep -f "socat pty,link=$evsesources2,raw tcp:$evselanips2:26" > /dev/null
				then
					echo "test" > /dev/null
				else
					sudo socat pty,link=$evsesources2,raw tcp:$evselanips2:26 &
				fi
			else
				echo "echo" > /dev/null
			fi	
			sudo python /var/www/html/openWB/runs/evsewritemodbus.py $evsesources2 $evseids2 6
		fi
		if [[ $evsecons2 == "simpleevsewifi" ]]; then
			output=$(curl --connect-timeout $evsewifitimeoutlp3 -s http://$evsewifiiplp3/getParameters)
			state=$(echo $output | jq '.list[] | .evseState')
			if ((state == false)) ; then
				curl --silent --connect-timeout $evsewifitimeoutlp3 -s http://$evsewifiiplp3/setStatus?active=true > /dev/null
			fi
			current=$(echo $output | jq '.list[] | .actualCurrent')
			if (( current != 6 )) ; then
				curl --silent --connect-timeout $evsewifitimeoutlp3 -s http://$evsewifiiplp3/setCurrent?current=6 > /dev/null
			fi
		fi
		echo 1 > /var/www/html/openWB/ramdisk/ladestatuss2
		echo 6 > /var/www/html/openWB/ramdisk/llsolls2
	fi
echo 1 > /var/www/html/openWB/ramdisk/ladestatus
echo 6 > /var/www/html/openWB/ramdisk/llsoll
