#!/bin/bash

# -- start user pi enforcement
# normally the soc module runs as user pi
# when LP Configuration is stored, it is run as user www-data
# This leads to various permission problems
# if actual user is not pi, this restarts the script as user pi
usr=`id -nu`
if [ "$usr" != "pi" ]
then
	sudo -u pi -c bash "$0 $*"
	exit $?
fi
# -- ending user pi enforcement

export OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
export RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
export MODULEDIR=$(cd "$(dirname "$0")" && pwd)
LOGFILE="$RAMDISKDIR/soc.log"
DMOD="EVSOC"
export CHARGEPOINT=$1

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
		captcha_token=$i3captcha_tokens1
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
		captcha_token=$i3captcha_token
		;;
esac

# make sure folder data/i3 exists in openwb home folder
# can be executed by pi or www-data so we have to use sudo 
prepare_i3DataFolder(){
	dataFolder="${OPENWBBASEDIR}/data"
	i3Folder="${dataFolder}/i3"
	if [ ! -d $i3Folder ]
	then
		sudo mkdir -p $i3Folder
		f=soc_i3_cp1.json
		if [ -f $RAMDISKDIR/$f -a ! -f $i3Folder/$f ]; then
			cp $RAMDISKDIR/$f $i3Folder
		fi
		f=soc_i3_cp2.json
		if [ -f $RAMDISKDIR/$f -a ! -f $i3Folder/$f ]; then
			cp $RAMDISKDIR/$f $i3Folder
		fi
	fi
	sudo chown -R pi:pi $dataFolder
	sudo chmod 0777 $i3Folder
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
	soctimer=$((soctimer + ticksize))
	echo $soctimer > "$soctimerfile"
}

prepare_i3DataFolder
soctimer=$(<"$soctimerfile")
openwbDebugLog ${DMOD} 2 "Lp$CHARGEPOINT: timer = $soctimer"
cd $MODULEDIR
if (( soctimer < (6 * intervall) )); then
	if(( soccalc < 1 )); then
		openwbDebugLog ${DMOD} 2 "Lp$CHARGEPOINT: Nothing to do yet. Incrementing timer."
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

		python3 "$MODULEDIR/manual.py" "$ARGSB64" &>> $LOGFILE &

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
	ARGS+='"captcha_token": "'"$captcha_token"'", '
	ARGS+='"debugLevel": "'"$DEBUGLEVEL"'"'
	ARGS+='}'

	ARGSB64=$(echo -n $ARGS | base64 --wrap=0)

	python3 "$MODULEDIR/i3soc.py" "$ARGSB64" &>> $LOGFILE &

	soclevel=$(<"$socfile")
	openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: SoC: $soclevel"

fi
