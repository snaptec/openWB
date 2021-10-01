#!/bin/bash
if (( pvkitversion == 1 )); then
	python /var/www/html/openWB/modules/wr_ethmpm3pmaevu/readlovato.py 
elif (( pvkitversion == 2 )); then
	python /var/www/html/openWB/modules/wr_ethmpm3pmaevu/readsdm.py
else
	python /var/www/html/openWB/modules/wr_ethmpm3pmaevu/readmpm3pm.py 
fi
pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)
echo $pvwatt
