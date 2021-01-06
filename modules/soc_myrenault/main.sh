#!/bin/bash

CHARGEPOINT=$1

case $CHARGEPOINT in
	2)
		# second charge point
		soctimerfile="/var/www/html/openWB/ramdisk/soctimer1"
		soc=$(</var/www/html/openWB/ramdisk/soc1)
		lstate=$(</var/www/html/openWB/ramdisk/ladestatuss1)
		plugstatus=$(</var/www/html/openWB/ramdisk/plugstats1)
		chagerstatus=$(</var/www/html/openWB/ramdisk/chargestats1)
		r8=$(</var/www/html/openWB/ramdisk/zoereply8lp2)
		username=$myrenault_userlp2
		password=$myrenault_passlp2
		location=$myrenault_locationlp2
		country=$myrenault_countrylp2
		wakeup=$wakeupmyrenaultlp2
		vin=$soclp2_vin
		;;
	*)
		# defaults to first charge point for backward compatibility
		CHARGEPOINT=1
		soctimerfile="/var/www/html/openWB/ramdisk/soctimer"
		soc=$(</var/www/html/openWB/ramdisk/soc)
		lstate=$(</var/www/html/openWB/ramdisk/ladestatus)
		plugstatus=$(</var/www/html/openWB/ramdisk/plugstat)
		chagerstatus=$(</var/www/html/openWB/ramdisk/chargestat)
		r8=$(</var/www/html/openWB/ramdisk/zoereply8lp1)
		username=$myrenault_userlp1
		password=$myrenault_passlp1
		location=$myrenault_locationlp1
		country=$myrenault_countrylp1
		wakeup=$wakeupmyrenaultlp1
		vin=$soclp1_vin
		;;
esac

timer=$(<$soctimerfile)
if (( timer < 60 )); then
	timer=$((timer+1))
	echo $timer > $soctimerfile
else
	echo 0 > $soctimerfile
	sudo python /var/www/html/openWB/modules/soc_myrenault/zoensoc.py $username $password $location $country $vin $CHARGEPOINT

	dtime=$(date +"%T")
	charging=$(echo $r8 | jq -r .data.attributes.chargingStatus)
	if [[ $lstate == "1" ]] && [[ $chagerstatus == "0" ]] && [[ $plugstatus == "1" ]] && [[ $charging == '-1' ]] && [[ $soc -ne 100 ]] && [[ $wakeup == "1" ]] ; then
		echo " $dtime zoe p$CHARGEPOINT ladung remote gestartet"
		echo " $dtime zoe p$CHARGEPOINT lstate(wallbox) $lstate plugged(Wallbox) $plugstatus charging(Wallbox) $chagerstatus charging(Zoe) $charging scheduler(zoe) $scheduler soc $soc "
		sudo python /var/www/html/openWB/modules/soc_myrenault/zoenwake.py $username $password $location $country $vin $CHARGEPOINT
	fi
fi
