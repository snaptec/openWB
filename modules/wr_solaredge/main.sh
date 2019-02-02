#!/bin/bash
. /var/www/html/openWB/openwb.conf

if [[ $solaredgepvslave3 != "none" ]] && [[ $solaredgepvslave2 != "none" ]]; then
	sudo python /var/www/html/openWB/modules/wr_solaredge/solaredge3.py $solaredgepvip $solaredgepvslave1 $solaredgepvslave2 $solaredgepvslave3
else
	if (( $solaredgepvslave2 != "none" )); then
		sudo python /var/www/html/openWB/modules/wr_solaredge/solaredge2.py $solaredgepvip $solaredgepvslave1 $solaredgepvslave2
	else
		sudo python /var/www/html/openWB/modules/wr_solaredge/solaredge.py $solaredgepvip $solaredgepvslave1
	fi

fi


pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)
echo $pvwatt

