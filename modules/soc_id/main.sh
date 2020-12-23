#!/bin/bash
soctimer=$(</var/www/html/openWB/ramdisk/soctimer)
ladeleistung=$(</var/www/html/openWB/ramdisk/llaktuell)


tmpintervall=$(( 480 * 6 ))

if (( soctimer < tmpintervall )); then
	soctimer=$((soctimer+1))
	if (( ladeleistung > 500 ));then
		soctimer=$((soctimer+47))
	fi
	echo $soctimer > /var/www/html/openWB/ramdisk/soctimer
else
	/var/www/html/openWB/modules/evcc-soc id --user "$soc_id_username" --password "$soc_id_passwort" --vin "$soc_id_vin" > /var/www/html/openWB/ramdisk/soc &
	echo 0 > /var/www/html/openWB/ramdisk/soctimer
fi
