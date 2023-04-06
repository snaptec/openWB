#!/bin/bash
if [[ $evseconlp7 == "extopenwb" ]]; then
	/var/www/html/openWB/modules/extopenwb/main.sh 7 $chargep7ip
else
	sudo python /var/www/html/openWB/modules/mpm3pmlllp7/readmpm3pm.py $mpmlp7ip $mpmlp7id
fi
