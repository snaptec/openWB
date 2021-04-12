#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
LOGFILE="$RAMDISKDIR/soc.log"
CHARGEPOINT=$1
socDebug=$debug
# for developement only
socDebug=1
touch $RAMDISKDIR/zoereply8lp1
touch $RAMDISKDIR/zoereply8lp2
case $CHARGEPOINT in
	2)
		# second charge point
		soctimerfile="$RAMDISKDIR/soctimer1"
		soc=$(<$RAMDISKDIR/soc1)
		lstate=$(<$RAMDISKDIR/ladestatuss1)
		plugstatus=$(<$RAMDISKDIR/plugstats1)
		chagerstatus=$(<$RAMDISKDIR/chargestats1)
		r8=$(<$RAMDISKDIR/zoereply8lp2)
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
		soctimerfile="$RAMDISKDIR/soctimer"
		soc=$(<$RAMDISKDIR/soc)
		lstate=$(<$RAMDISKDIR/ladestatus)
		plugstatus=$(<$RAMDISKDIR/plugstat)
		chagerstatus=$(<$RAMDISKDIR/chargestat)
		r8=$(<$RAMDISKDIR/zoereply8lp1)
		username=$myrenault_userlp1
		password=$myrenault_passlp1
		location=$myrenault_locationlp1
		country=$myrenault_countrylp1
		wakeup=$wakeupmyrenaultlp1
		vin=$soclp1_vin
		;;
esac

socDebugLog(){
	if (( $socDebug > 0 )); then
		timestamp=`date +"%Y-%m-%d %H:%M:%S"`
		echo "$timestamp: Lp$CHARGEPOINT: $@" >> $LOGFILE
	fi
}

timer=$(<$soctimerfile)
if (( timer < 60 )); then
	socDebugLog "Nothing to do yet. Incrementing timer."
	timer=$((timer+1))
	echo $timer > $soctimerfile
else
	echo 0 > $soctimerfile
	socDebugLog "Requesting SoC"
	sudo python /var/www/html/openWB/modules/soc_myrenault/zoensoc.py $username $password $location $country $vin $CHARGEPOINT
	case $CHARGEPOINT in
		2)
			# second charge point
			soc=$(<$RAMDISKDIR/soc1)
			;;
		*)
			# defaults to first charge point for backward compatibility
			soc=$(<$RAMDISKDIR/soc)
			;;
	esac
	socDebugLog "SoC from Server: $soc"
	dtime=$(date +"%T")
	charging=$(echo $r8 | jq -r .data.attributes.chargingStatus)
	if [[ $lstate == "1" ]] && [[ $chagerstatus == "0" ]] && [[ $plugstatus == "1" ]] && [[ $charging == '-1' ]] && [[ $soc -ne 100 ]] && [[ $wakeup == "1" ]] ; then
		socDebugLog "zoe ladung remote gestartet"
		socDebugLog "zoe lstate(wallbox) $lstate plugged(Wallbox) $plugstatus charging(Wallbox) $chagerstatus charging(Zoe) $charging scheduler(zoe) $scheduler soc $soc "
		sudo python /var/www/html/openWB/modules/soc_myrenault/zoenwake.py $username $password $location $country $vin $CHARGEPOINT
	fi
fi
