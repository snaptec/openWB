#!/bin/bash

if [[ $mpm3pmllsource = *virtual* ]]
then
	if ps ax |grep -v grep |grep "socat pty,link=$mpm3pmllsource,raw tcp:$sdm630modbuslllanip:26" > /dev/null
	then
		echo "test" > /dev/null
	else
		sudo socat pty,link=$mpm3pmllsource,raw tcp:$sdm630modbuslllanip:26 &
	fi
else
	echo "echo" > /dev/null
fi
sudo python /var/www/html/openWB/modules/mpm3pmll/readmpm3pm.py $mpm3pmllsource $mpm3pmllid



