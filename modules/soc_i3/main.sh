#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd "$(dirname "$0")" && pwd)
LOGFILE="$RAMDISKDIR/soc.log"
DMOD="EVSOC"
CHARGEPOINT=$1

# check if config file is already in env
if [[ -z "$debug" ]]; then
	echo "soc_i3: seems like openwb.conf is not loaded. Reading file."
	# try to load config
	. "$OPENWBBASEDIR/loadconfig.sh"
	# load helperFunctions
	. "$OPENWBBASEDIR/helperFunctions.sh"
fi

DEBUGLEVEL=$debug

case $CHARGEPOINT in
	2)
		# second charge point
		soctimerfile="$RAMDISKDIR/soctimer1"
		socfile="$RAMDISKDIR/soc1"
		meterfile="$RAMDISKDIR/llkwhs1"
		statefile="$RAMDISKDIR/soc_i3_lp2_state"
		soccalc=$i3_soccalclp2
		batterysize=$akkuglp2
		efficiency=$wirkungsgradlp2
		intervall=$soci3intervall1
		user=$i3usernames1
		pass=$i3passworts1
		vin=$i3vins1
		;;
	*)
		# defaults to first charge point for backward compatibility
		# set CHARGEPOINT in case it is empty (needed for logging)
		CHARGEPOINT=1
		soctimerfile="$RAMDISKDIR/soctimer"
		socfile="$RAMDISKDIR/soc"
		meterfile="$RAMDISKDIR/llkwh"
		statefile="$RAMDISKDIR/soc_i3_lp1_state"
		soccalc=$i3_soccalclp1
		batterysize=$akkuglp1
		efficiency=$wirkungsgradlp2
		intervall=$soci3intervall
		user=$i3username
		pass=$i3passwort
		vin=$i3vin
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
	soctimer=$((soctimer + ticksize))
	echo $soctimer > "$soctimerfile"
}

soctimer=$(<"$soctimerfile")
openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: timer = $soctimer"
cd $MODULEDIR
if (( soctimer < (6 * intervall) )); then
	if(( soccalc < 1 )); then
		openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: Nothing to do yet. Incrementing timer."
	else
		ARGS='{'
		ARGS+='"socfile": "'"$socfile"'", '
		ARGS+='"meterfile": "'"$meterfile"'", '
		ARGS+='"statefile": "'"$statefile"'", '
		ARGS+='"batterysize": "'"$batterysize"'", '
		ARGS+='"efficiency": "'"$efficiency"'", '
		ARGS+='"debugLevel": "'"$DEBUGLEVEL"'"'
		ARGS+='}'

		ARGSB64=$(echo -n $ARGS | base64 --wrap=0)

		sudo python3 "$MODULEDIR/manual.py" "$ARGSB64" &>> $LOGFILE &

		soclevel=$(<"$socfile")
		openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: SoC: $soclevel"
	fi
	incrementTimer
else
	openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: Requesting SoC"
	echo 0 > "$soctimerfile"

	ARGS='{'
	ARGS+='"user": "'"$user"'", '
	ARGS+='"pass": "'"$pass"'", '
	ARGS+='"vin": "'"$vin"'", '
	ARGS+='"socfile": "'"$socfile"'", '
	ARGS+='"meterfile": "'"$meterfile"'", '
	ARGS+='"statefile": "'"$statefile"'", '
	ARGS+='"debugLevel": "'"$DEBUGLEVEL"'"'
	ARGS+='}'

	ARGSB64=$(echo -n $ARGS | base64 --wrap=0)

	sudo python3 "$MODULEDIR/i3soc.py" "$ARGSB64" &>> $LOGFILE &

	soclevel=$(<"$socfile")
	openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: SoC: $soclevel"

fi
