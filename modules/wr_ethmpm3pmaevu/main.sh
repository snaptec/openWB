#!/bin/bash
if (( pvkitversion == 1 )); then
	sudo python /var/www/html/openWB/modules/wr_ethmpm3pmaevu/readlovato.py 
else
	sudo python /var/www/html/openWB/modules/wr_ethmpm3pmaevu/readmpm3pm.py 
fi
pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)
echo $pvwatt


