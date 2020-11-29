#!/bin/bash

if [[ $modbusevsesourcelp2 = *virtual* ]]
then
	if ps ax |grep -v grep |grep "socat pty,link=$modbusevsesourcelp2,raw tcp:$modbusevselaniplp2:26" > /dev/null
	then
		echo "test" > /dev/null
	else
		sudo socat pty,link=$modbusevsesourcelp2,raw tcp:$modbusevselaniplp2:26 &
	fi
else
	echo "echo" > /dev/null
fi
sudo python /var/www/html/openWB/modules/mpm3pmlls1/readmpm3pm.py $mpm3pmllsourcelp2 $mpm3pmllidlp2



