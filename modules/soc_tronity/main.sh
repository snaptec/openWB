#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
DMOD="EVSOC"
CHARGEPOINT=$1

# check if config file is already in env
if [[ -z "$debug" ]]; then
	echo "soc_tronity: Seems like openwb.conf is not loaded. Reading file."
	# try to load config
	. $OPENWBBASEDIR/loadconfig.sh
	# load helperFunctions
	. $OPENWBBASEDIR/helperFunctions.sh
fi

case $CHARGEPOINT in
	2)
		# second charge point
		ladeleistungfile="$RAMDISKDIR/llaktuells1"
		soctimerfile="$RAMDISKDIR/soctimer1"
		soc_file="$RAMDISKDIR/soc1"
		soc_tronity_client_id=$soc_tronity_client_id_lp2
		soc_tronity_client_secret=$soc_tronity_client_secret_lp2
		soc_tronity_vehicle_id=$soc_tronity_vehicle_id_lp2
		socintervall=$soc2intervall
		socintervallladen=$soc2intervallladen
		tokensfile="$MODULEDIR/tokens.lp2"
		;;
	*)
		# defaults to first charge point for backward compatibility
		# set CHARGEPOINT in case it is empty (needed for logging)
		CHARGEPOINT=1
		ladeleistungfile="$RAMDISKDIR/llaktuell"
		soctimerfile="$RAMDISKDIR/soctimer"
		soc_file="$RAMDISKDIR/soc"
		soc_tronity_client_id=$soc_tronity_client_id_lp1
		soc_tronity_client_secret=$soc_tronity_client_secret_lp1
		soc_tronity_vehicle_id=$soc_tronity_vehicle_id_lp1
		socintervall=$soc_tronity_intervall
		socintervallladen=$soc_tronity_intervallladen
		tokensfile="$MODULEDIR/tokens.lp1"
		;;
esac

getAndWriteSoc(){
	re='^-?[0-9]+$'
	url="https://api.tronity.tech/tronity/vehicles/${soc_tronity_vehicle_id}/last_record"
	response=$(curl --silent --connect-timeout 15 --header 'Authorization: bearer '${authToken} ${url})
	if [[ "$response" =~ '"level"' ]]; then
		soclevel=$(echo $response | jq --raw-output .level)
		if  [[ $soclevel =~ $re ]] ; then
			if (( $soclevel != 0 )) ; then
				echo $soclevel > $soc_file
				openwbDebugLog ${DMOD} 0 "Lp$CHARGEPOINT: SoC: $soclevel"
			fi
		fi
	else
		errCode=$(echo $response | jq .statusCode)
		errText=$(echo $response | jq .message)
		openwbDebugLog ${DMOD} 0 "Lp$CHARGEPOINT: ERROR: Requesting SoC failed!"
		openwbModulePublishState "EVSOC" 2 "SoC-Abfrage fehlgeschlagen! $errCode $errText" $CHARGEPOINT
	fi
}

login(){
	returnValue=0
	# TODO: Check if we have a valid access_token
	if [ -f $tokensfile ]; then
		openwbDebugLog ${DMOD} 2 "Lp$CHARGEPOINT: token present."
		tokentime=$(stat -c %Y $tokensfile)
		validity=$(cat $tokensfile | jq --raw-output .expires_in)
		timestamp=$(date +%s)
		if (( tokentime + validity < timestamp )); then
			openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: removing expired token."
			rm $tokensfile
		else
			openwbDebugLog ${DMOD} 2 "Lp$CHARGEPOINT: token stil valid."
			authToken=$(cat $tokensfile | jq --raw-output .access_token)
		fi
	fi
	if [ ! -f $tokensfile ]; then
		openwbDebugLog ${DMOD} 0 "Lp$CHARGEPOINT: requesting new token."
		response=$(curl --silent --connect-timeout 15 --header 'Content-Type: application/json' --request POST --data '{"client_id":"'${soc_tronity_client_id}'","client_secret":"'${soc_tronity_client_secret}'","grant_type": "app"}' https://api.tronity.tech/authentication)
		if  [[ "$response" =~ '"access_token"' ]]; then
			echo "$response" > $tokensfile
			openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: got new access_token."
			authToken=$(echo $response | jq --raw-output .access_token)
		else
			errCode=$(echo $response | jq .statusCode)
			errText=$(echo $response | jq .message)
			openwbDebugLog ${DMOD} 0 "Lp$CHARGEPOINT: ERROR: Auth with user/pass failed!"
			openwbModulePublishState "EVSOC" 2 "Anmeldung fehlgeschlagen! $errCode $errText" $CHARGEPOINT
			returnvalue=1
		fi
	fi
	return "$returnValue"
}

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

authToken=''
soctimer=$(<$soctimerfile)
openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: timer = $soctimer"
ladeleistung=$(<$ladeleistungfile)

if (( ladeleistung > 1000 )); then
	openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: Car is charging"
	timerToCheck=$socintervallladen
else
	openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: Car is not charging"
	timerToCheck=$socintervall
fi

if (( soctimer < timerToCheck )); then
	openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: Nothing to do yet. Incrementing timer."
	incrementTimer
else
	openwbDebugLog ${DMOD} 0 "Lp$CHARGEPOINT: Requesting SoC"
	echo 0 > $soctimerfile
	login
	checkResult=$?
	if [ "$checkResult" == 0 ]; then
		getAndWriteSoc
		checkResult=$?
		if [ "$checkResult" == 0 ]; then
			openwbModulePublishState "EVSOC" 0 "Erfolgreich" $CHARGEPOINT
		fi
	fi
fi
