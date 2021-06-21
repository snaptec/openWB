#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
LOGFILE="$RAMDISKDIR/soc.log"
CHARGEPOINT=$1

socDebug=$debug
# for developement only
socDebug=1

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

socDebugLog(){
	if (( $socDebug > 0 )); then
		timestamp=`date +"%Y-%m-%d %H:%M:%S"`
		echo "$timestamp: Lp$CHARGEPOINT: $@" >> $LOGFILE
	fi
}

timer=$(<$soctimerfile)
dtime=$(date +"%T")

if (( timer < 60 )); then
	socDebugLog "Nothing to do yet. Incrementing timer."
	timer=$((timer+1))
	echo $timer > $soctimerfile
else
	echo 0 > $soctimerfile
	socDebugLog "Requesting SoC"
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
		socDebugLog "zoe ladung remote gestartet"
		socDebugLog "zoe lstate(wallbox) $lstate plugged(Wallbox) $plugstatus charging(Wallbox) $chagerstatus charging(Zoe) $charging scheduler(zoe) $scheduler soc $soc "
		request3=$(curl -s -H "Content-Type: application/json" -X POST -H "Authorization: Bearer $token" https://www.services.renault-ze.com/api/vehicle/$vin/charge)
		echo 0 > $zoestatusfile
		echo $request3 > $request3file
	else
		if [[ $debug = "1" ]] ; then
			socDebugLog "zoe lstate(wallbox) $lstate plugged(Wallbox) $plugstatus charging(Wallbox) $chagerstatus charging(Zoe) $charging scheduler(zoe) $scheduler soc $soc wakeupzoe $wakeup"
		fi
	fi
fi
