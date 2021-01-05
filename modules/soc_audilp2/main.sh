#!/bin/bash

auditimer=$(</var/www/html/openWB/ramdisk/soctimer1)
if (( auditimer < 180 )); then
	auditimer=$((auditimer+1))
	if ((ladeleistung > 800 )); then
		auditimer=$((auditimer+2))
	fi
	echo $auditimer > /var/www/html/openWB/ramdisk/soctimer1
else
	echo 0 > /var/www/html/openWB/ramdisk/soctimer1
	/var/www/html/openWB/modules/evcc-soc audi --user "$soc2user" --password "$soc2pass" > /var/www/html/openWB/ramdisk/soc1
fi
