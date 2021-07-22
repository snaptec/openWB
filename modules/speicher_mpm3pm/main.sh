#!/bin/bash

if (( speicherkitversion == 1 )); then
	sudo python /var/www/html/openWB/modules/speicher_mpm3pm/readsdm120.py 
elif (( speicherkitversion == 2 )); then
	sudo python /var/www/html/openWB/modules/speicher_mpm3pm/readsdm630.py 
else
	sudo python /var/www/html/openWB/modules/speicher_mpm3pm/readmpm3pm.py 
fi
