#!/bin/bash
if [[ $evseconlp4 == "extopenwb" ]]; then
	/var/www/html/openWB/modules/extopenwb/main.sh 4 $chargep4ip
else
	sudo python /var/www/html/openWB/modules/mpm3pmlllp4/readmpm3pm.py $mpmlp4ip $mpmlp4id
fi
