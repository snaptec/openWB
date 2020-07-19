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
	sudo python3 /var/www/html/openWB/modules/soc_kia/kiasoc.py $soc_bluelink_email $soc_bluelink_password $soc_bluelink_pin $soc_vin &
	echo 0 > /var/www/html/openWB/ramdisk/soctimer
fi
