#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
DMOD="EVSOC"
CHARGEPOINT=$1

# check if config file is already in env
if [[ -z "$debug" ]]; then
	echo "soc_zoe: Seems like openwb.conf is not loaded. Reading file."
	# try to load config
	. $OPENWBBASEDIR/loadconfig.sh
	# load helperFunctions
	. $OPENWBBASEDIR/helperFunctions.sh
fi

case $CHARGEPOINT in
	2)
		# second charge point
		lstate=$(<$RAMDISKDIR/ladestatuss1)
		plugstatus=$(<$RAMDISKDIR/plugstats1)
		chagerstatus=$(<$RAMDISKDIR/chargestats1)
		soctimerfile="$RAMDISKDIR/soctimer1"
		username=$zoelp2username
		password=$zoelp2passwort
		socfile="$RAMDISKDIR/soc1"
		requestfile="$RAMDISKDIR/zoerequestlp2"
		request1file="$RAMDISKDIR/zoerequest1lp2"
		request2file="$RAMDISKDIR/zoerequest2lp2"
		request3file="$RAMDISKDIR/zoerequest3lp2"
		wakeup="wakeupzoelp2"
		zoestatusfile="$RAMDISKDIR/zoestatuslp2"
		;;
	*)
		# defaults to first charge point for backward compatibility
		# set CHARGEPOINT in case it is empty (needed for logging)
		CHARGEPOINT=1
		lstate=$(<$RAMDISKDIR/ladestatus)
		plugstatus=$(<$RAMDISKDIR/plugstat)
		chagerstatus=$(<$RAMDISKDIR/chargestat)
		soctimerfile="$RAMDISKDIR/soctimer"
		username=$zoeusername
		password=$zoepasswort
		socfile="$RAMDISKDIR/soc"
		requestfile="$RAMDISKDIR/zoerequest"
		request1file="$RAMDISKDIR/zoerequest1"
		request2file="$RAMDISKDIR/zoerequest2"
		request3file="$RAMDISKDIR/zoerequest3"
		wakeup="wakeupzoelp1"
		zoestatusfile="$RAMDISKDIR/zoestatus"
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

soctimer=$(<$soctimerfile)
openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: timer = $soctimer"
dtime=$(date +"%T")

if (( soctimer < 60 )); then
	openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: Nothing to do yet. Incrementing soctimer."
	incrementTimer
else
	echo 0 > $soctimerfile
	openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: Requesting SoC"
	request=$(curl -s -H "Content-Type: application/json" -X POST -d '{"username":"'$username'","password":"'$password'"}' https://www.services.renault-ze.com/api/user/login)
	token=$(echo $request | jq -r .token)
	vin=$(echo $request | jq -r .user.vehicle_details.VIN)
	request1=$(curl -s -H "Authorization: Bearer $token" https://www.services.renault-ze.com/api/vehicle/$vin/battery)
	soc=$(echo $request1 | jq .charge_level)
	request2=$(curl -s -H "Authorization: Bearer $token" https://www.services.renault-ze.com/api/vehicle/$vin/charge/scheduler/onboard)
	scheduler=$(echo $request2 | jq .enabled)
	charging=$(echo $request1 | jq .charging)
	#save what we get

	echo $request > $requestfile
	echo $request1 > $request1file
	echo $request2 > $request2file
	echo $soc > $socfile
	if [[ $lstate == "1" ]] && [[ $chagerstatus == "0" ]] && [[ $plugstatus == "1" ]] && [[ $scheduler == "false" ]] && [[ $soc -ne 100 ]] && [[ $charging == "false" ]] && [[ $wakeup == "1" ]] ; then
		openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: zoe ladung remote gestartet"
		openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: zoe lstate(wallbox) $lstate plugged(Wallbox) $plugstatus charging(Wallbox) $chagerstatus charging(Zoe) $charging scheduler(zoe) $scheduler soc $soc "
		request3=$(curl -s -H "Content-Type: application/json" -X POST -H "Authorization: Bearer $token" https://www.services.renault-ze.com/api/vehicle/$vin/charge)
		echo 0 > $zoestatusfile
		echo $request3 > $request3file
	else
		if [[ $debug = "1" ]] ; then
			openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: zoe lstate(wallbox) $lstate plugged(Wallbox) $plugstatus charging(Wallbox) $chagerstatus charging(Zoe) $charging scheduler(zoe) $scheduler soc $soc wakeupzoe $wakeup"
		fi
	fi
fi
