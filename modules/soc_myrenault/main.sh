#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
DMOD="EVSOC"
CHARGEPOINT=$1

# check if config file is already in env
if [[ -z "$debug" ]]; then
	echo "soc_myrenault: Seems like openwb.conf is not loaded. Reading file."
	# try to load config
	. $OPENWBBASEDIR/loadconfig.sh
	# load helperFunctions
	. $OPENWBBASEDIR/helperFunctions.sh
fi

case $CHARGEPOINT in
	2)
		# second charge point
		soctimerfile="$RAMDISKDIR/soctimer1"
		socfile="$RAMDISKDIR/soc1"
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
		socfile="$RAMDISKDIR/soc"
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

incrementTimer(){
	case $dspeed in
		1)
			# Regelgeschwindigkeit 10 Sekunden
			ticksize=1
			;;
		2)
			# Regelgeschwindigkeit 20 Sekunden
			ticksize=2
			;;
		3)
			# Regelgeschwindigkeit 60 Sekunden
			ticksize=1
			;;
		*)
			# Regelgeschwindigkeit unbekannt
			ticksize=1
			;;
	esac
	soctimer=$((soctimer+$ticksize))
	echo $soctimer > $soctimerfile
}

touch $RAMDISKDIR/zoereply8lp1
touch $RAMDISKDIR/zoereply8lp2

soctimer=$(<$soctimerfile)
openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: timer = $soctimer"
if (( soctimer < 60 )); then
	openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: Nothing to do yet. Incrementing timer."
	incrementTimer
else
	echo 0 > $soctimerfile
	openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: Requesting SoC"
	sudo python /var/www/html/openWB/modules/soc_myrenault/zoensoc.py $username $password $location $country $vin $CHARGEPOINT
	soc=$(<$socfile)
	openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: SoC from Server: $soc"
	dtime=$(date +"%T")
	charging=$(echo $r8 | jq -r .data.attributes.chargingStatus)
	if [[ $lstate == "1" ]] && [[ $chagerstatus == "0" ]] && [[ $plugstatus == "1" ]] && [[ $charging == '-1' ]] && [[ $soc -ne 100 ]] && [[ $wakeup == "1" ]] ; then
		openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: zoe ladung remote gestartet"
		openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: zoe lstate(wallbox) $lstate plugged(Wallbox) $plugstatus charging(Wallbox) $chagerstatus charging(Zoe) $charging scheduler(zoe) $scheduler soc $soc "
		sudo python /var/www/html/openWB/modules/soc_myrenault/zoenwake.py $username $password $location $country $vin $CHARGEPOINT
	fi
fi
