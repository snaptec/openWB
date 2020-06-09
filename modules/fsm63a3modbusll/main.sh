#!/bin/bash

### TODO: The following variables need to be added to "openwb.conf":
# fsm63a3modbusllsource=... (e.g. "/dev/ttyUSB0")
# fsm63a3modbusllid=... (e.g. "2")
### Furthermore the following value in "openwb.conf" has to be set manually:
# ladeleistungmodul=fsm63a3modbusll
### If once all three values can be set up via the GUI (needs to be done by snaptec), these 6 lines can be deleted.

if [[ $fsm63a3llsource = *virtual* ]]
then
	if ps ax |grep -v grep |grep "socat pty,link=$fsm63a3llsource,raw tcp:$fsm63a3modbuslllanip:26" > /dev/null
	then
		echo "test" > /dev/null
	else
		sudo socat pty,link=$fsm63a3llsource,raw tcp:$fsm63a3modbuslllanip:26 &
	fi
else
	echo "echo" > /dev/null
fi

# Set the ramdisk path here (and don´t hard code it in the python script)
ramdiskpath="/var/www/html/openWB/ramdisk"

sudo python /var/www/html/openWB/modules/fsm63a3modbusll/readfsm63a3.py $fsm63a3modbusllsource $fsm63a3modbusllid $ramdiskpath

