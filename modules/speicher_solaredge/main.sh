#!/bin/bash
if [[ $solaredgespeicherip == $solaredgepvip ]]  ; then
	echo "value read at pv modul" > /dev/null
else
	python /var/www/html/openWB/modules/speicher_solaredge/solaredge.py $solaredgespeicherip $solaredgezweiterspeicher
fi
