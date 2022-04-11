#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
DMOD="EVSOC"
CHARGEPOINT=$1

# check if config file is already in env
if [[ -z "$debug" ]]; then
	echo "soc_audi: Seems like openwb.conf is not loaded. Reading file."
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
		username=$soc2user
		password=$soc2pass
		vin=$soc2vin
		;;
	*)
		# defaults to first charge point for backward compatibility
		# set CHARGEPOINT in case it is empty (needed for logging)
		CHARGEPOINT=1
		soctimerfile="$RAMDISKDIR/soctimer"
		socfile="$RAMDISKDIR/soc"
		username=$soc_audi_username
		password=$soc_audi_passwort
		vin=$soc_audi_vin
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
	# special handling for this soc module
	if ((ladeleistung > 800 )); then
		ticksize=$((ticksize*2))
	fi
	soctimer=$((soctimer+$ticksize))
	echo $soctimer > $soctimerfile
}

soctimer=$(<$soctimerfile)
openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: timer = $soctimer"
if (( soctimer < 180 )); then
	openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: Charging, but nothing to do yet. Incrementing timer."
	incrementTimer
else
	echo 0 > $soctimerfile
	openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: Requesting SoC"
	answer=$($MODULEDIR/../evcc-soc audi --user "$username" --password "$password" --vin "$vin" 2>&1)
	if [ $? -eq 0 ]; then
 		# we got a valid answer
 		echo $answer > $socfile
 		openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: SoC: $answer"
 	else
 		# we have a problem
 		openwbDebugLog ${DMOD} 0 "Lp$CHARGEPOINT: Error from evcc-soc: $answer"
 	fi
fi
