#!/bin/bash

. /var/www/html/openWB/openwb.conf

i3timer=$(</var/www/html/openWB/ramdisk/soctimer1)
cd /var/www/html/openWB/modules/soc_i3s1
if (( i3timer < 60 )); then
	i3timer=$((i3timer+1))
	echo $i3timer > /var/www/html/openWB/ramdisk/soctimer1
else
	re='^-?[0-9]+$'
	abfrage=$(sudo php index.php | jq '.')
	soclevel=$(echo $abfrage | jq '.chargingLevel')
	if  [[ $soclevel =~ $re ]] ; then
		if (( $soclevel != 0 )) ; then
			echo $soclevel > /var/www/html/openWB/ramdisk/soc1
		fi
	fi

#Abfrage Ladung aktiv. Setzen des soctimers. 
	charging=$(echo $abfrage | jq '.chargingActive')
	if [[ $charging != 0 ]] ; then
		soctimer1=$((60 * (10 - $soci3intervall1) / 10))
		echo $soctimer1 > /var/www/html/openWB/ramdisk/soctimer1
	else
		echo 1 > /var/www/html/openWB/ramdisk/soctimer1
	fi

#Benachrichtigung bei Ladeabbruch 
	charging=$(echo $abfrage | jq '.chargingActive')
    	if [ "$charging" = "CHARGINGERROR" ] ; then
        	message="ACHTUNG - Ladung bei "
        	message+="$soclevel"
        	message+="% abgebrochen"
		/var/www/html/openWB/runs/pushover.sh "$message"
	fi
fi
