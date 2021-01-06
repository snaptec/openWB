#!/bin/bash

CHARGEPOINT=$1

case $CHARGEPOINT in
	2)
		# second charge point
		soctimerfile="/var/www/html/openWB/ramdisk/soctimer1"
		socfile="/var/www/html/openWB/ramdisk/soc1"
		intervall=$soccarnetlp2intervall
		username=$carnetlp2user
		password=$carnetlp2pass
		;;
	*)
		# defaults to first charge point for backward compatibility
		soctimerfile="/var/www/html/openWB/ramdisk/soctimer"
		socfile="/var/www/html/openWB/ramdisk/soc"
		intervall=$soccarnetintervall
		username=$carnetuser
		password=$carnetpass
		;;
esac

vwtimer=$(<$soctimerfile)
if (( vwtimer < 60 )); then
	vwtimer=$((vwtimer+1))
	echo $vwtimer > $soctimerfile
else
	echo 0 > $soctimerfile
	/var/www/html/openWB/modules/soc_carnet/soc.sh $username $password
	#Abfrage Ladung aktiv. Setzen des soctimers. 
	if (( ladeleistung > 800 )) ; then
		vwtimer=$((60 * (10 - $intervall) / 10))
		echo $vwtimer > $soctimerfile
	fi
	
	/var/www/html/openWB/modules/soc_carnet/soc.sh $username $password $socfile
fi
