#!/bin/bash
if [[ $evseconlp8 == "extopenwb" ]]; then
	/var/www/html/openWB/modules/extopenwb/main.sh 8 $chargeiplp8
else
	sudo python /var/www/html/openWB/modules/mpm3pmlllp8/readmpm3pm.py $mpmiplp8 $mpmidlp8
fi


