#!/bin/bash
soctimer=$(</var/www/html/openWB/ramdisk/soctimer)



tmpintervall=$(( 720 * 6 ))

if (( soctimer < tmpintervall )); then
	soctimer=$((soctimer+1))
	echo $soctimer > /var/www/html/openWB/ramdisk/soctimer
else
	/var/www/html/openWB/modules/evcc-soc id --user "$soc_id_username" --password "$soc_id_passwort" --vin "$soc_id_vin" > /var/www/html/openWB/ramdisk/soc &
	echo 0 > /var/www/html/openWB/ramdisk/soctimer
fi
