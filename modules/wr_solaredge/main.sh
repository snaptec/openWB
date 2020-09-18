#!/bin/bash

Solaredgebatwr="0"
if [[ $solaredgespeicherip == $solaredgepvip ]]  ; then
	 Solaredgebatwr="1"  
fi
if [[ $solaredgepvslave3 != "none" ]] && [[ $solaredgepvslave4 != "none" ]]&& [[ $solaredgepvslave2 != "none" ]]; then
	sudo python /var/www/html/openWB/modules/wr_solaredge/solaredge4.py $solaredgepvip $solaredgepvslave1 $solaredgepvslave2 $solaredgepvslave3 $Solaredgebatwr $solaredgepvslave4 $wr1extprod
else
	if [[ $solaredgepvslave3 != "none" ]] && [[ $solaredgepvslave2 != "none" ]]; then
		sudo python /var/www/html/openWB/modules/wr_solaredge/solaredge3.py $solaredgepvip $solaredgepvslave1 $solaredgepvslave2 $solaredgepvslave3 $Solaredgebatwr $wr1extprod
	else
		if (( $solaredgepvslave2 != "none" )); then
			sudo python /var/www/html/openWB/modules/wr_solaredge/solaredge2.py $solaredgepvip $solaredgepvslave1 $solaredgepvslave2 $Solaredgebatwr $wr1extprod
		else
			if [[ $solaredgewr2ip != "none" ]]; then
				sudo python /var/www/html/openWB/modules/wr_solaredge/solaredge2wr.py $solaredgepvip $solaredgepvslave1 $Solaredgebatwr $solaredgewr2ip	$wr1extprod
			else
				sudo python /var/www/html/openWB/modules/wr_solaredge/solaredge.py $solaredgepvip $solaredgepvslave1 $Solaredgebatwr $wr1extprod
			fi
		fi
	fi
fi

pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)
echo $pvwatt

