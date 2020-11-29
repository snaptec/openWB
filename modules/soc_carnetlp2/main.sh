#!/bin/bash


vwtimer=$(</var/www/html/openWB/ramdisk/soctimer1)
if (( vwtimer < 60 )); then
	vwtimer=$((vwtimer+1))
	echo $vwtimer > /var/www/html/openWB/ramdisk/soctimer1
else
	/var/www/html/openWB/modules/soc_carnetlp2/soc.sh $carnetuserlp2 $carnetpasslp2 &
	#Abfrage Ladung aktiv. Setzen des soctimers.

	if (( ladeleistung > 800 )) ; then
		vwtimer=$((60 * (10 - $soccarnetintervalllp2) / 10))
		echo $vwtimer > /var/www/html/openWB/ramdisk/soctimer1
	else
		echo 1 > /var/www/html/openWB/ramdisk/soctimer1
	fi
fi
