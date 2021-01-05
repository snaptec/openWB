#!/bin/bash

CHARGEPOINT=$1

case $CHARGEPOINT in
	2) 
		# second charge point
		soctimerfile="/var/www/html/openWB/ramdisk/soctimer1"
		socfile="/var/www/html/openWB/ramdisk/soc1"
		username=$soc2user
		password=$soc2pass
		;;
	*)
		# defaults to first charge point for backward compatibility
		# set CHARGEPOINT in case it is empty (needed for logging)
		CHARGEPOINT=1
		soctimerfile="/var/www/html/openWB/ramdisk/soctimer"
		socfile="/var/www/html/openWB/ramdisk/soc"
		username=$soc_audi_username
		password=$soc_audi_passwort
		;;
esac

auditimer=$(<$soctimerfile)
if (( auditimer < 180 )); then
	auditimer=$((auditimer+1))
	if ((ladeleistung > 800 )); then
		auditimer=$((auditimer+2))
	fi
	echo $auditimer > $soctimerfile
else
	/var/www/html/openWB/modules/evcc-soc audi --user "$username" --password "$passsword" > $socfile &
	echo 1 > $soctimerfile
fi
