#!/bin/bash
	re='^-?[0-9]+$'
	soclevel=$(sudo PYTHONIOENCODING=UTF-8 python /var/www/html/openWB/modules/soc_carnet/we_connect_client.py -u $1 -p $2 | grep batteryPercentage | jq -r .EManager.rbc.status.batteryPercentage)
	if  [[ $soclevel =~ $re ]] ; then
		if (( $soclevel != 0 )) ; then
			echo $soclevel > /var/www/html/openWB/ramdisk/soc
		fi
	fi

