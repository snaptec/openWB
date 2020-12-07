#!/bin/bash
soctimer=$(</var/www/html/openWB/ramdisk/soctimer)



tmpintervall=$(( soc_id_interval * 6 ))

if (( soctimer < tmpintervall )); then
	soctimer=$((soctimer+1))
	echo $soctimer > /var/www/html/openWB/ramdisk/soctimer
else
	/var/www/html/openWB/modules/evcc-soc id --user $soc_id_email --password $soc_id_password --pin $soc_id_vin > /var/www/html/openWB/ramdisk/soc &
	echo 0 > /var/www/html/openWB/ramdisk/soctimer
fi
