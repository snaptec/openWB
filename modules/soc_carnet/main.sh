#!/bin/bash


vwtimer=$(</var/www/html/openWB/ramdisk/soctimer)
if (( vwtimer < 60 )); then
	vwtimer=$((vwtimer+1))
	echo $vwtimer > /var/www/html/openWB/ramdisk/soctimer
else
	/var/www/html/openWB/modules/soc_carnet/soc.sh $carnetuser $carnetpass &
	#Abfrage Ladung aktiv. Setzen des soctimers. 
	
	if (( ladeleistung > 800 )) ; then
		vwtimer=$((60 * (10 - $soccarnetintervall) / 10))
		echo $vwtimer > /var/www/html/openWB/ramdisk/soctimer
	else
		echo 1 > /var/www/html/openWB/ramdisk/soctimer
	fi
fi
