#!/bin/bash
OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
DMOD="EVSOC"
CHARGEPOINT=$1
export OPENWBBASEDIR RAMDISKDIR MODULEDIR

export debug=1

# check if config file is already in env
if [[ -z "$debug" ]]; then
	echo "soc_smarteq: Seems like openwb.conf is not loaded. Reading file."
	# try to load config
	. $OPENWBBASEDIR/loadconfig.sh
	# load helperFunctions
	. $OPENWBBASEDIR/helperFunctions.sh
fi

case $CHARGEPOINT in
	2)
		# second charge point
		ladeleistung=$(<$RAMDISKDIR/llaktuells1)
		soctimerfile="$RAMDISKDIR/soctimer1"
		socfile="$RAMDISKDIR/soc1"
		fztype=$soc2type
		username=$soc2user
		password=$soc2pass
		pin=$soc2pint
		vin=$soc2vin
		intervall=$(( soc2intervall * 6 ))
		intervallladen=$(( soc2intervallladen * 6 ))
		;;
	*)
		# defaults to first charge point for backward compatibility
		# set CHARGEPOINT in case it is empty (needed for logging)
		CHARGEPOINT=1
		ladeleistung=$(<$RAMDISKDIR/llaktuell)
		soctimerfile="$RAMDISKDIR/soctimer"
		socfile="$RAMDISKDIR/soc"
		username=$soc_smarteq_username
		password=$soc_smarteq_passwort
		pin=$soc_smarteq_pin
		vin=$soc_smarteq_vin
		intervall=$(( soc_smarteq_intervall * 6 ))
		intervallladen=$(( soc_smarteq_intervallladen * 6 ))
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

getAndWriteSoc(){
	openwbDebugLog ${DMOD} 2 "Lp$CHARGEPOINT: Requesting SoC"
	echo 0 > $soctimerfile

	if [ "$password" != "" ]
	then
		answer=$($MODULEDIR/soc_smarteq_pass.py --user "$username" --password "$password" --vin "$vin" --chargepoint "$CHARGEPOINT" 2>>$RAMDISKDIR/soc.log)
	else
		answer=$($MODULEDIR/soc_smarteq_2fa.py --user "$username" --pin "$pin" --vin "$vin" --chargepoint "$CHARGEPOINT" 2>>$RAMDISKDIR/soc.log)
	fi
	if [ $? -eq 0 ]; then
		# we got a valid answer
		echo $answer > $socfile
		openwbDebugLog ${DMOD} 2 "Lp$CHARGEPOINT: SoC: $answer"
	else
		# we have a problem
		openwbDebugLog ${DMOD} 0 "Lp$CHARGEPOINT: Error from soc_smart: $answer"
	fi
}

soctimer=$(<$soctimerfile)
if (( ladeleistung > 500 )); then
	if (( soctimer < intervallladen )); then
		openwbDebugLog ${DMOD} 2 "Lp$CHARGEPOINT: Charging, but nothing to do yet. Incrementing timer."
		incrementTimer
	else
		getAndWriteSoc
	fi
else
	if (( soctimer < intervall )); then
		openwbDebugLog ${DMOD} 2 "Lp$CHARGEPOINT: Nothing to do yet. Incrementing timer."
		incrementTimer

	else
		getAndWriteSoc
	fi
fi

