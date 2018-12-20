#!/bin/bash

#Variable aus openWB uebergeben. Verkuerzte Intervallzeit in Prozent waehrend Ladevogang.
i3socintervall=10

i3timer=$(</var/www/html/openWB/ramdisk/soctimer)
cd /var/www/html/openWB/modules/soc_i3
if (( i3timer < 60 )); then
	i3timer=$((i3timer+1))
	echo $i3timer > /var/www/html/openWB/ramdisk/soctimer
else
	re='^-?[0-9]+$'
	soclevel=$(sudo php index.php | jq .chargingLevel)
	if  [[ $soclevel =~ $re ]] ; then
		if (( $soclevel != 0 )) ; then
			echo $soclevel > /var/www/html/openWB/ramdisk/soc
		fi
	fi

#Abfrage Ladung aktiv. Setzen des soctimers. 
	charging=$(echo $abfrage | jq '.chargingActive')
	if (( $charging != 0 )) ; then
		soctimer=$((60 * (100 - $i3socintervall) / 100))
		echo $soctimer > /var/www/html/openWB/ramdisk/soctimer
	else
		echo 0 > /var/www/html/openWB/ramdisk/soctimer
	fi
fi
