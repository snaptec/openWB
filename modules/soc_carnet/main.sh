#!/bin/bash

OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd "$(dirname "$0")" && pwd)
DMOD="EVSOC"
CHARGEPOINT=$1

# check if config file is already in env
if [[ -z "$debug" ]]; then
	echo "soc_carnet: Seems like openwb.conf is not loaded. Reading file."
	# try to load config
	. "$OPENWBBASEDIR/loadconfig.sh"
	# load helperFunctions
	. "$OPENWBBASEDIR/helperFunctions.sh"
fi

case $CHARGEPOINT in
	2)
		# second charge point
		soctimerfile="$RAMDISKDIR/soctimer1"
		socfile="$RAMDISKDIR/soc1"
		intervall=$soccarnetlp2intervall
		username=$carnetlp2user
		password=$carnetlp2pass
		;;
	*)
		# defaults to first charge point for backward compatibility
		# set CHARGEPOINT in case it is empty (needed for logging)
		CHARGEPOINT=1
		soctimerfile="$RAMDISKDIR/soctimer"
		socfile="$RAMDISKDIR/soc"
		intervall=$soccarnetintervall
		username=$carnetuser
		password=$carnetpass
		;;
esac

reValidSoc='^-?[0-9]+$'

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
	soctimer=$((soctimer + ticksize))
	echo $soctimer > "$soctimerfile"
}

soctimer=$(<"$soctimerfile")
openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: timer = $soctimer"
if (( soctimer < 60 )); then
	openwbDebugLog ${DMOD} 2 "Lp$CHARGEPOINT: Nothing to do yet. Incrementing timer."
	incrementTimer
else
	openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: Requesting SoC"
	#Abfrage Ladung aktiv. Hochsetzen des soctimers, um das Intervall zu verkürzen.
	if (( ladeleistung > 800 )) ; then
		soctimer=$((60 * (10 - intervall) / 10))
		echo $soctimer > "$soctimerfile"
	else
		echo 0 > "$soctimerfile"
	fi

	response=$(sudo PYTHONIOENCODING=UTF-8 python "$MODULEDIR/we_connect_client.py" --user="$username" --password="$password")
	soclevel=$(echo "$response" | grep batteryPercentage | jq -r .EManager.rbc.status.batteryPercentage)
	openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: Filtered SoC from Server: $soclevel"
	if  [[ $soclevel =~ $reValidSoc ]] ; then
		if (( soclevel != 0 )) ; then
			openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: SoC is valid"
			echo "$soclevel" > "$socfile"
		fi
	else
		openwbDebugLog ${DMOD} 0 "Lp$CHARGEPOINT: SoC is not valid."
		openwbDebugLog ${DMOD} 0 "Lp$CHARGEPOINT: Response from Server: ${response}"
	fi

fi
