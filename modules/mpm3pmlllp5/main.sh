#!/bin/bash
if [[ $evseconlp5 == "extopenwb" ]]; then
		/var/www/html/openWB/modules/extopenwb/main.sh 5 $chargeiplp5
else
	sudo python /var/www/html/openWB/modules/mpm3pmlllp5/readmpm3pm.py $mpmiplp5 $mpmidlp5
fi


