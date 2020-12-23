#!/bin/bash
soctimer=$(</var/www/html/openWB/ramdisk/soctimer)

#soc_bluelink_email='xxx@xxx.xxx'
#soc_bluelink_password='xxx'
#soc_bluelink_pin='xxx'
#soc_bluelink_interval='5'

tmpintervall=$(( soc_bluelink_interval * 6 ))

if (( soctimer < tmpintervall )); then
	soctimer=$((soctimer+1))
	echo $soctimer > /var/www/html/openWB/ramdisk/soctimer
else
	/var/www/html/openWB/modules/evcc-soc hyundai --user $soc_bluelink_email --password $soc_bluelink_password --pin $soc_bluelink_pin > /var/www/html/openWB/ramdisk/soc &
	echo 0 > /var/www/html/openWB/ramdisk/soctimer
fi
