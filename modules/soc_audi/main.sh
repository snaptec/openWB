#!/bin/bash

auditimer=$(</var/www/html/openWB/ramdisk/soctimer)
if (( auditimer < 180 )); then
	auditimer=$((auditimer+1))
	if ((ladeleistung > 800 )); then
		auditimer=$((auditimer+2))
	fi
	echo $auditimer > /var/www/html/openWB/ramdisk/soctimer
else
	echo 0 > /var/www/html/openWB/ramdisk/soctimer
	/var/www/html/openWB/modules/evcc-soc audi --user "$soc_audi_username" --password "$soc_audi_passwort" > /var/www/html/openWB/ramdisk/soc
fi
