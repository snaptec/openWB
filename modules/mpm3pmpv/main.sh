#!/bin/bash

if [[ $mpm3pmpvsource = *virtual* ]]
then
	if ps ax |grep -v grep |grep "socat pty,link=$mpm3pmpvsource,raw tcp:$mpm3pmpvlanip:26" > /dev/null
	then
		echo "test" > /dev/null
	else
		sudo socat pty,link=$mpm3pmpvsource,raw tcp:$mpm3pmpvlanip:26 &
	fi
else
	echo "echo" > /dev/null
fi
sudo python /var/www/html/openWB/modules/mpm3pmpv/readmpm3pm.py $mpm3pmpvsource $mpm3pmpvid
pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)
echo $pvwatt
