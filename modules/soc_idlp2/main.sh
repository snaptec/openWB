#!/bin/bash
soctimer=$(</var/www/html/openWB/ramdisk/soctimer1)
ladeleistung=$(</var/www/html/openWB/ramdisk/llaktuells1)


tmpintervall=$(( 480 * 6 ))

if (( soctimer < tmpintervall )); then
	soctimer=$((soctimer+1))
	if (( ladeleistung > 500 ));then
		soctimer=$((soctimer+47))
	fi
	echo $soctimer > /var/www/html/openWB/ramdisk/soctimer1
else
	/var/www/html/openWB/modules/evcc-soc id --user "$soc2user" --password "$soc2pass" --vin "$soc2vin" > /var/www/html/openWB/ramdisk/soc1 &
	echo 0 > /var/www/html/openWB/ramdisk/soctimer1
fi
