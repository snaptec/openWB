#!/bin/bash

i3timer=$(</var/www/html/openWB/ramdisk/soctimer1)
cd /var/www/html/openWB/modules/soc_i3s1
if (( i3timer < 60 )); then
	i3timer=$((i3timer+1))
	echo $i3timer > /var/www/html/openWB/ramdisk/soctimer1
else
	re='^-?[0-9]+$'
	soclevel=$(sudo php index.php | jq .chargingLevel)
	if  [[ $soclevel =~ $re ]] ; then
		echo $soclevel > /var/www/html/openWB/ramdisk/soc1
	fi
	echo 0 > /var/www/html/openWB/ramdisk/soctimer1
fi
