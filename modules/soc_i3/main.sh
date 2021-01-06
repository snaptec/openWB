#!/bin/bash

CHARGEPOINT=$1

case $CHARGEPOINT in
	2)
		# second charge point
		soctimerfile="/var/www/html/openWB/ramdisk/soctimer1"
		socfile="/var/www/html/openWB/ramdisk/soc1"
		intervall=$soci3intervall1
		;;
	*)
		# defaults to first charge point for backward compatibility
		soctimerfile="/var/www/html/openWB/ramdisk/soctimer"
		socfile="/var/www/html/openWB/ramdisk/soc"
		intervall=$soci3intervall
		;;
esac

i3timer=$(<$soctimerfile)
cd /var/www/html/openWB/modules/soc_i3
if (( i3timer < 60 )); then
	i3timer=$((i3timer+1))
	echo $i3timer > $soctimerfile
else
	echo 0 > /var/www/html/openWB/ramdisk/soctimer
	re='^-?[0-9]+$'
	abfrage=$(sudo php index.php?chargepoint=$CHARGEPOINT | jq '.')
	soclevel=$(echo $abfrage | jq '.chargingLevel')
	if  [[ $soclevel =~ $re ]] ; then
		if (( $soclevel != 0 )) ; then
			echo $soclevel > $socfile
		fi
	fi

	#Abfrage Ladung aktiv. Setzen des soctimers.
	charging=$(echo $abfrage | jq '.chargingActive')
	if [[ $charging != 0 ]] ; then
		soctimer=$((60 * (10 - $intervall) / 10))
		echo $soctimer > $soctimerfile
	fi

	#Benachrichtigung bei Ladeabbruch
	error=$(echo $abfrage | jq '.chargingError')
	if [[ $error == 1 ]] && [[ $pushbenachrichtigung == 1 ]] ; then
		#Abfrage, ob Fehler schon dokumentiert
		chargingError=$(</var/www/html/openWB/ramdisk/chargingerror)
		#wiederholte Benachrichtigungen verhindern
		if [[ $chargingError == 0 ]] ; then
			message="ACHTUNG - Ladung bei "
			message+="$soclevel"
			message+="% abgebrochen"
			/var/www/html/openWB/runs/pushover.sh "$message"
			#dokumetieren des Fehlers in der Ramdisk
			echo 1 > /var/www/html/openWB/ramdisk/chargingerror
		fi
	else
		echo 0 > /var/www/html/openWB/ramdisk/chargingerror
	fi
fi
