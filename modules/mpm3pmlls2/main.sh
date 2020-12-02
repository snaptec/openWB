#!/bin/bash

if [[ $modbusevsesourcelp3 = *virtual* ]]
then
	if ps ax |grep -v grep |grep "socat pty,link=$modbusevsesourcelp3,raw tcp:$modbusevselaniplp3:26" > /dev/null
	then
		echo "test" > /dev/null
	else
		sudo socat pty,link=$modbusevsesourcelp3,raw tcp:$modbusevselaniplp3:26 &
	fi
else
	echo "echo" > /dev/null
fi
sudo python /var/www/html/openWB/modules/mpm3pmlls2/readmpm3pm.py $mpm3pmllsourcelp3 $mpm3pmllidlp3



