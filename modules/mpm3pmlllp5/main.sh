#!/bin/bash
if [[ $evseconlp5 == "extopenwb" ]]; then
	/var/www/html/openWB/modules/extopenwb/main.sh 5 $chargep5ip
else
	sudo python /var/www/html/openWB/modules/mpm3pmlllp5/readmpm3pm.py $mpmlp5ip $mpmlp5id
fi
