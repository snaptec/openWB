#!/bin/bash
if [[ $evseconlp6 == "extopenwb" ]]; then
	/var/www/html/openWB/modules/extopenwb/main.sh 6 $chargeiplp6
else
	sudo python /var/www/html/openWB/modules/mpm3pmlllp6/readmpm3pm.py $mpmiplp6 $mpmidlp6
fi


