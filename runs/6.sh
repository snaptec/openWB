#!/bin/bash
. /var/www/html/openWB/openwb.conf
if [[ $evsecon == "dac" ]]; then
	sudo python /var/www/html/openWB/runs/dac.py 790 $dacregister
fi
if [[ $evsecon == "modbusevse" ]]; then
	if [[ $modbusevsesource = *virtual* ]]
	then
		if ps ax |grep -v grep |grep "socat pty,link=$modbusevsesource,raw tcp:$modbusevselanip:26" > /dev/null
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
			if ps ax |grep -v grep |grep "socat pty,link=$evsesources1,raw tcp:$evselanips1:26" > /dev/null
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
				if ps ax |grep -v grep |grep "socat pty,link=$evsesources2,raw tcp:$evselanips2:26" > /dev/null
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
		echo 1 > /var/www/html/openWB/ramdisk/ladestatuss2
		echo 6 > /var/www/html/openWB/ramdisk/llsolls2
	fi
echo 1 > /var/www/html/openWB/ramdisk/ladestatus
echo 6 > /var/www/html/openWB/ramdisk/llsoll
