#!/bin/bash

if [[ $mpm3pmspeichersource = *virtual* ]]
then
	if ps ax |grep -v grep |grep "socat pty,link=$mpm3pmspeichersource,raw tcp:$mpm3pmspeicherlanip:26" > /dev/null
	then
		echo "test" > /dev/null
	else
		sudo socat pty,link=$mpm3pmspeichersource,raw tcp:$mpm3pmspeicherlanip:26 &
	fi
else
	echo "echo" > /dev/null
fi
sudo python /var/www/html/openWB/modules/mpm3pmspeicher/readmpm3pm.py $mpm3pmspeichersource $mpm3pmspeicherid $mpm3pmspeicherpv
