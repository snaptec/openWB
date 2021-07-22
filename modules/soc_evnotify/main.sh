#!/bin/bash
OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
CONFIGFILE="$OPENWBBASEDIR/openwb.conf"
DMOD="EVSOC"
CHARGEPOINT=$1

# check if config file is already in env
if [[ -z "$debug" ]]; then
	echo "soc_evnotify: Seems like openwb.conf is not loaded. Reading file."
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
		akey=$evnotifyakeylp2
		token=$evnotifytokenlp2
		;;
	*)
		# defaults to first charge point for backward compatibility
		# set CHARGEPOINT in case it is empty (needed for logging)
		CHARGEPOINT=1
		soctimerfile="$RAMDISKDIR/soctimer"
		socfile="$RAMDISKDIR/soc"
		akey=$evnotifyakey
		token=$evnotifytoken
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
if (( soctimer < 4 )); then
	openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: Nothing to do yet. Incrementing timer."
	incrementTimer
else
	openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: Requesting SoC"
	echo 0 > $soctimerfile
	answer=$(curl -s -X GET 'https://app.evnotify.de/soc?akey='$akey'&token='$token)
	# extract the soc value
	soc=$(echo $answer | jq .soc_display)
	openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: SoC from Server: $soc"
	# parse to int to be able to check in condition - to determine if valid or not
	isvalid=$(echo $soc | cut -d "." -f 1 | cut -d "," -f 1)
	if (( isvalid >= 0 && isvalid != null)); then
		echo $isvalid > $socfile
	else
		openwbDebugLog ${DMOD} 0 "Lp$CHARGEPOINT: SoC is invalid!"
	fi
fi
