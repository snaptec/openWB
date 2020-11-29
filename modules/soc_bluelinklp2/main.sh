#!/bin/bash
soctimer=$(</var/www/html/openWB/ramdisk/soctimer1)

tmpintervall=120

if (( soctimer < tmpintervall )); then
	soctimer=$((soctimer+1))
	echo $soctimer > /var/www/html/openWB/ramdisk/soctimer1
else
	/var/www/html/openWB/modules/evcc-soc hyundai --user $socuserlp2 --password $socpasslp2 --pin $soc_bluelink_pinlp2 > /var/www/html/openWB/ramdisk/soc1 &
	echo 0 > /var/www/html/openWB/ramdisk/soctimer1
fi
