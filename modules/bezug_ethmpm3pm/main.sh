#!/bin/bash
if (( evukitversion == 1 )); then
	sudo python /var/www/html/openWB/modules/bezug_ethmpm3pm/readlovato.py
else
	sudo python /var/www/html/openWB/modules/bezug_ethmpm3pm/readmpm3pm.py 
fi
wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug


