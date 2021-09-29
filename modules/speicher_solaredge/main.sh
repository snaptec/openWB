#!/bin/bash
if [[ $solaredgespeicherip == $solaredgepvip ]]  ; then
	echo "value read at pv modul" > /dev/null
else
	python3 /var/www/html/openWB/packages/modules/bat/solaredge.py "${solaredgespeicherip}" "${solaredgezweiterspeicher}"
fi
