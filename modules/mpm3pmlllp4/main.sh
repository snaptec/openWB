#!/bin/bash
if [[ $evseconlp4 == "extopenwb" ]]; then
	/var/www/html/openWB/modules/extopenwb/main.sh 4 $chargeiplp4
else
	sudo python /var/www/html/openWB/modules/mpm3pmlllp4/readmpm3pm.py $mpmiplp4 $mpmidlp4
fi


