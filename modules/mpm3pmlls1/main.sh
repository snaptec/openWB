#!/bin/bash

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
sudo python /var/www/html/openWB/modules/mpm3pmlls1/readmpm3pm.py $mpm3pmlls1source $mpm3pmlls1id
