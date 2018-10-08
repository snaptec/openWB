#!/bin/bash
. /var/www/html/openWB/openwb.conf

if [[ $mpm3pmevusource = *virtual* ]]
then
	if ps ax |grep -v grep |grep "socat pty,link=$mpm3pmevusource,raw tcp:$sdm630modbuslllanip:26" > /dev/null
	then
		echo "test" > /dev/null
	else
		sudo socat pty,link=$mpm3pmevusource,raw tcp:$sdm630modbuslllanip:26 &
	fi
else
	echo "echo" > /dev/null
fi
sudo python /var/www/html/openWB/modules/bezug_mpm3pm/readmpm3pm.py $mpm3pmevusource $mpm3pmevuid



