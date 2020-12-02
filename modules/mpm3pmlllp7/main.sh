#!/bin/bash
if [[ $evseconlp7 == "extopenwb" ]]; then
	/var/www/html/openWB/modules/extopenwb/main.sh 7 $chargeiplp7
else
	sudo python /var/www/html/openWB/modules/mpm3pmlllp7/readmpm3pm.py $mpmiplp7 $mpmidlp7
fi


