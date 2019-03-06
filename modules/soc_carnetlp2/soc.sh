#!/bin/bash
	re='^-?[0-9]+$'
	soclevel=$(sudo python /var/www/html/openWB/modules/soc_carnetlp2/vw_carnet_rb1.py $1 $2 | grep batteryPercentage | jq -r .EManager.rbc.status.batteryPercentage)
	if  [[ $soclevel =~ $re ]] ; then
		if (( $soclevel != 0 )) ; then
			echo $soclevel > /var/www/html/openWB/ramdisk/soc1
		fi
	fi

